#!/usr/bin/env python3
"""
Export authorized Chaoxing/Xuexitong course resources from a logged-in browser:
1) Homework + in-class quiz questions to JSON/DOCX
2) Chapter courseware attachments (ppt/pptx/pdf/doc/docx) to local files
"""

from __future__ import annotations

import argparse
import asyncio
import html
import json
import re
import time
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path
from typing import Any
from xml.sax.saxutils import escape

import requests
import websockets
from bs4 import BeautifulSoup


TYPE_MAP = {
    0: "单选题",
    1: "多选题",
    2: "填空题",
    3: "判断题",
    4: "简答题",
    5: "名词解释",
    6: "论述题",
    7: "计算题",
    9: "填空题",
    10: "填空题",
    16: "判断题",
    18: "口语题",
}

DOWNLOAD_EXTS = {".ppt", ".pptx", ".pdf", ".doc", ".docx"}
SOURCE_LABELS = {"quiz": "随堂练习", "homework": "作业"}
ANSWER_SOURCE_LABELS = {"chaoxing": "学习通答案", "unpublished": "未公开", "model": "模型推断"}


def clean_text(value: Any) -> str:
    if value is None:
        return ""
    value = html.unescape(str(value))
    soup = BeautifulSoup(value, "html.parser")
    for br in soup.find_all("br"):
        br.replace_with("\n")
    text = soup.get_text("\n")
    text = re.sub(r"\r", "", text)
    text = re.sub(r"[ \t\xa0]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n", text)
    return text.strip()


def safe_name(name: str) -> str:
    name = re.sub(r'[\\/:*?"<>|]+', "_", name).strip()
    name = re.sub(r"\s+", " ", name)
    return name[:180] or "untitled"


def normalize_question_type(value: Any) -> str:
    if isinstance(value, int):
        return TYPE_MAP.get(value, f"未知题型({value})")
    text = clean_text(value)
    if text.isdigit():
        return TYPE_MAP.get(int(text), f"未知题型({text})")
    aliases = {
        "Single Choice": "单选题",
        "Multiple Choice": "多选题",
        "Fill Blank": "填空题",
        "True/False": "判断题",
        "Short Answer": "简答题",
        "Term Explanation": "名词解释",
        "Essay": "论述题",
        "Calculation": "计算题",
        "Oral": "口语题",
        "单选": "单选题",
        "多选": "多选题",
        "填空": "填空题",
        "判断": "判断题",
        "简答": "简答题",
    }
    return aliases.get(text, text)


def is_true_false_type(qtype: Any) -> bool:
    return normalize_question_type(qtype) == "判断题"


def normalize_true_false_value(value: Any, index: int | None = None) -> str:
    text = clean_text(value)
    compact = re.sub(r"[\s.。:：、）)]", "", text).upper()
    if compact in {"1", "A", "TRUE", "T", "YES", "Y", "RIGHT", "CORRECT", "√", "✓", "对", "是", "正确"}:
        return "对"
    if compact in {"2", "B", "FALSE", "F", "NO", "N", "WRONG", "INCORRECT", "×", "✗", "错", "否", "错误"}:
        return "错"
    if any(marker in text for marker in ["正确", "对", "是", "TRUE", "True", "true", "√", "✓"]):
        return "对"
    if any(marker in text for marker in ["错误", "错", "否", "FALSE", "False", "false", "×", "✗"]):
        return "错"
    if index == 0:
        return "对"
    if index == 1:
        return "错"
    return text


def normalize_answer_for_type(value: Any, qtype: Any) -> str:
    text = clean_text(value)
    if not text or not is_true_false_type(qtype):
        return text
    parts = re.split(r"([,，;；/、\s]+)", text)
    normalized = [normalize_true_false_value(part) if part.strip() else part for part in parts]
    return "".join(normalized).strip() or text


def format_quiz_option(qtype: Any, option: dict[str, Any], index: int) -> str:
    name = clean_text(option.get("name"))
    content = clean_text(option.get("content"))
    if is_true_false_type(qtype):
        return normalize_true_false_value(content or name, index)
    if name and content:
        return f"{name}. {content}"
    return name or content


def format_homework_option(qtype: Any, text: str, index: int) -> str:
    text = clean_text(text)
    if is_true_false_type(qtype):
        return normalize_true_false_value(text, index)
    return text


class CDP:
    def __init__(self, cdp_base: str):
        self.cdp_base = cdp_base.rstrip("/")
        self._idx = 0

    def tabs(self) -> list[dict[str, Any]]:
        with urllib.request.urlopen(f"{self.cdp_base}/json/list") as response:
            return json.load(response)

    def find_tab(self, pattern: str = "chaoxing.com") -> dict[str, Any]:
        for tab in self.tabs():
            if pattern in tab.get("url", "") and tab.get("type") == "page":
                return tab
        raise RuntimeError(f"No browser tab matched {pattern!r}. Open the course page first.")

    async def call(self, ws, method: str, params: dict[str, Any] | None = None, timeout: int = 60):
        self._idx += 1
        msg_id = self._idx
        await ws.send(json.dumps({"id": msg_id, "method": method, "params": params or {}}))
        while True:
            msg = json.loads(await asyncio.wait_for(ws.recv(), timeout=timeout))
            if msg.get("id") == msg_id:
                return msg

    async def cookies(self) -> list[dict[str, Any]]:
        tab = self.find_tab("chaoxing.com")
        async with websockets.connect(tab["webSocketDebuggerUrl"], max_size=80_000_000) as ws:
            return (await self.call(ws, "Network.getAllCookies"))["result"]["cookies"]

    async def course_state(self) -> dict[str, Any]:
        tab = self.find_tab("mooc2-ans.chaoxing.com/mooc2-ans/mycourse/stu")
        async with websockets.connect(tab["webSocketDebuggerUrl"], max_size=80_000_000) as ws:
            await self.call(ws, "Runtime.enable")
            result = await self.call(
                ws,
                "Runtime.evaluate",
                {
                    "expression": """(() => ({
                        href: location.href,
                        title: document.title
                    }))()""",
                    "returnByValue": True,
                    "awaitPromise": True,
                },
            )
            return result["result"]["result"]["value"]

    async def homework_list_url(self) -> str | None:
        tab = self.find_tab("mooc2-ans.chaoxing.com/mooc2-ans/mycourse/stu")
        async with websockets.connect(tab["webSocketDebuggerUrl"], max_size=80_000_000) as ws:
            await self.call(ws, "Runtime.enable")
            result = await self.call(
                ws,
                "Runtime.evaluate",
                {
                    "expression": """(() => {
                        const existing = document.querySelector('#frame_content-zy');
                        if (existing && existing.src) return existing.src;
                        const link = document.querySelector('li[dataname="zy"] a[data-url], a[title="作业"][data-url]');
                        if (link) link.click();
                        return '';
                    })()""",
                    "returnByValue": True,
                    "awaitPromise": True,
                },
            )
            value = result["result"]["result"].get("value") or ""
            if value:
                return value
            for _ in range(20):
                await asyncio.sleep(0.5)
                result = await self.call(
                    ws,
                    "Runtime.evaluate",
                    {
                        "expression": "(() => document.querySelector('#frame_content-zy')?.src || '')()",
                        "returnByValue": True,
                        "awaitPromise": True,
                    },
                )
                value = result["result"]["result"].get("value") or ""
                if value:
                    return value
        return None


def make_session(cookies: list[dict[str, Any]]) -> requests.Session:
    session = requests.Session()
    session.trust_env = False
    session.headers.update(
        {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/148 Safari/537.36",
            "Referer": "https://mooc2-ans.chaoxing.com/",
        }
    )
    for cookie in cookies:
        session.cookies.set(cookie["name"], cookie["value"], domain=cookie.get("domain"), path=cookie.get("path", "/"))
    return session


def query(url: str) -> dict[str, str]:
    return dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(url).query))


def parse_homework_list(
    session: requests.Session,
    course_id: str,
    class_id: str,
    cpi: str,
    list_url: str | None = None,
) -> list[dict[str, str]]:
    url = list_url or f"https://mooc1.chaoxing.com/mooc2/work/list?courseId={course_id}&classId={class_id}&cpi={cpi}&ut=s&t={int(time.time() * 1000)}"
    soup = BeautifulSoup(session.get(url, timeout=40).text, "html.parser")
    works = []
    for li in soup.select('li[onclick*="goTask"]'):
        task_url = html.unescape(li.get("data") or "")
        name = clean_text((li.select_one(".right-content p:first-child") or li).get_text(" "))
        status_el = li.select_one("p.status")
        works.append({"source": "homework", "name": name, "status": clean_text(status_el.get_text(" ")) if status_el else "", "url": task_url})
    return [item for item in works if item["url"]]


def parse_homework_page(session: requests.Session, work: dict[str, str], course_id: str, class_id: str, cpi: str) -> list[dict[str, Any]]:
    response = session.get(work["url"], timeout=40, allow_redirects=True)
    soup = BeautifulSoup(response.text, "html.parser")
    if not soup.select(".questionLi"):
        hidden = {key: (soup.select_one(f"#{key}") or {}).get("value") for key in ["workId", "answerId", "enc", "standardEnc"]}
        if all(hidden.values()):
            retry = (
                "https://mooc1.chaoxing.com/mooc-ans/mooc2/work/view"
                f"?courseId={course_id}&classId={class_id}&cpi={cpi}&workId={hidden['workId']}"
                f"&answerId={hidden['answerId']}&standardEnc={hidden['standardEnc']}&enc={hidden['enc']}"
            )
            soup = BeautifulSoup(session.get(retry, timeout=40).text, "html.parser")

    title_el = soup.select_one(".mark_title") or soup.select_one("h2")
    title = clean_text(title_el.get_text(" ")) if title_el else work["name"]
    questions = []
    for q in soup.select(".questionLi"):
        name_el = q.select_one(".mark_name")
        raw = clean_text(name_el.get_text(" ", strip=True)) if name_el else ""
        match = re.match(r"^(\d+)\.\s*(?:\(([^)]+)\))?\s*(.*)$", raw, flags=re.S)
        num = match.group(1) if match else str(len(questions) + 1)
        qtype = normalize_question_type(match.group(2) if match and match.group(2) else "")
        stem = match.group(3).strip() if match else raw
        answer = normalize_answer_for_type(q.select_one(".rightAnswerContent").get_text(" ", strip=True), qtype) if q.select_one(".rightAnswerContent") else ""
        student_answer = normalize_answer_for_type(q.select_one(".stuAnswerContent").get_text(" ", strip=True), qtype) if q.select_one(".stuAnswerContent") else ""
        item = {
            "source": "homework",
            "set": title,
            "status": work.get("status", ""),
            "num": num,
            "type": qtype,
            "stem": stem,
            "options": [format_homework_option(qtype, li.get_text(" ", strip=True), idx) for idx, li in enumerate(q.select(".qtDetail li"))],
            "student_answer": student_answer,
            "answer": answer,
            "analysis": clean_text(q.select_one(".qtAnalysis").get_text(" ", strip=True)) if q.select_one(".qtAnalysis") else "",
        }
        item["answer_source"] = "chaoxing" if item["answer"] else "unpublished"
        questions.append(item)
    return questions


def parse_activity_list(session: requests.Session, fid: str, course_id: str, class_id: str) -> list[dict[str, str]]:
    url = "https://mobilelearn.chaoxing.com/v2/apis/active/student/activelist"
    payload = session.get(
        url,
        params={"fid": fid, "courseId": course_id, "classId": class_id, "showNotStartedActive": "0"},
        timeout=40,
    ).json()
    data = ((payload.get("data") or {}).get("activeList")) or []
    return [
        {"source": "quiz", "name": a.get("nameOne") or f"quiz-{a.get('id')}", "status": str(a.get("status")), "id": str(a.get("id"))}
        for a in data
        if str(a.get("activeType")) == "42"
    ]


def answer_from_quiz_question(question: dict[str, Any]) -> str:
    qtype = normalize_question_type(question.get("type"))
    for key in ["rightAnswer", "answerStr", "answerResult", "standardAnswer", "correctAnswer", "answerContent"]:
        if question.get(key) not in [None, "", []]:
            return normalize_answer_for_type(question.get(key), qtype)
    letters = []
    for option in question.get("answer") or []:
        if option.get("isanswer") in [1, "1", True] or option.get("isRight") in [1, "1", True] or option.get("right") in [1, "1", True]:
            letters.append(normalize_answer_for_type(option.get("name") or option.get("content"), qtype))
    return "".join(letters)


def student_quiz_answer(question: dict[str, Any], qtype: Any) -> str:
    person = question.get("personAnswer") or {}
    if person.get("myoption") not in [None, ""]:
        return normalize_answer_for_type(person.get("myoption"), qtype)
    if person.get("blankAnswer"):
        return "; ".join(f"{clean_text(x.get('name'))}:{clean_text(x.get('content'))}" for x in person.get("blankAnswer") or [])
    return normalize_answer_for_type(person.get("content"), qtype)


def parse_quiz(session: requests.Session, activity: dict[str, str]) -> list[dict[str, Any]]:
    response = session.get("https://mobilelearn.chaoxing.com/v2/apis/studentQuestion/getAnswerResult", params={"activeId": activity["id"]}, timeout=40).json()
    if response.get("result") != 1:
        response = session.get(
            "https://mobilelearn.chaoxing.com/v2/apis/quiz/quizDetail2",
            params={"activeId": activity["id"], "moreClassAttendEnc": "", "DB_STRATEGY": "PRIMARY_KEY", "STRATEGY_PARA": "activeId"},
            timeout=40,
        ).json()
    data = response.get("data") or {}
    qlist = data.get("questionList") or data.get("questionlist") or []
    active = data.get("active") or data.get("pptActive") or {}
    title = active.get("name") or activity["name"]

    questions = []
    for idx, question in enumerate(qlist, 1):
        qtype = normalize_question_type(question.get("type"))
        answer = answer_from_quiz_question(question)
        item = {
            "source": "quiz",
            "set": title,
            "status": "ongoing" if activity.get("status") == "1" else "ended",
            "num": str(idx),
            "type": qtype,
            "stem": clean_text(question.get("content")),
            "options": [
                option
                for option in [format_quiz_option(qtype, o, option_idx) for option_idx, o in enumerate(question.get("answer") or [])]
                if option
            ],
            "student_answer": student_quiz_answer(question, qtype),
            "answer": answer,
            "analysis": clean_text(question.get("analysis") or question.get("answerAnalysis") or question.get("resolve")),
            "answer_source": "chaoxing" if answer else "unpublished",
        }
        questions.append(item)
    return questions


def chapter_items(session: requests.Session, course_id: str, class_id: str, cpi: str) -> list[dict[str, str]]:
    url = "https://mooc2-ans.chaoxing.com/mooc2-ans/mycourse/studentcourse"
    response = session.get(
        url,
        params={"courseid": course_id, "clazzid": class_id, "cpi": cpi, "ut": "s"},
        timeout=40,
    )
    soup = BeautifulSoup(response.text, "html.parser")
    items = []
    for node in soup.select(".chapter_item"):
        onclick = node.get("onclick") or ""
        match = re.search(r"toOld\(\s*['\"]?\d+['\"]?\s*,\s*['\"]?([0-9]+)['\"]?\s*,", onclick)
        if not match:
            continue
        title = clean_text(node.get("title") or node.get_text(" ")) or f"chapter-{match.group(1)}"
        items.append({"knowledgeid": match.group(1), "title": title})
    dedup = {}
    for item in items:
        dedup[item["knowledgeid"]] = item
    return list(dedup.values())


def extract_attachments_from_cards(cards_html: str) -> list[dict[str, str]]:
    attachments: list[dict[str, str]] = []
    soup = BeautifulSoup(cards_html, "html.parser")
    for frame in soup.select('iframe[module="insertdoc"][data]'):
        try:
            data = json.loads(html.unescape(frame.get("data") or "{}"))
        except json.JSONDecodeError:
            continue
        object_id = clean_text(data.get("objectid"))
        name = clean_text(data.get("name") or data.get("title"))
        if object_id:
            attachments.append({"objectid": object_id, "name": name})
    for block in re.finditer(r'"objectid"\s*:\s*"([^"]+)".{0,600}?"name"\s*:\s*"([^"]+)"', cards_html, flags=re.S):
        object_id = block.group(1).strip()
        name = clean_text(block.group(2))
        attachments.append({"objectid": object_id, "name": name})
    dedup: dict[str, dict[str, str]] = {}
    for item in attachments:
        dedup[item["objectid"]] = item
    return list(dedup.values())


def resolve_download_url(session: requests.Session, object_id: str) -> tuple[str | None, str | None]:
    status_url = f"https://mooc1.chaoxing.com/ananas/status/{object_id}"
    response = session.get(status_url, params={"_dc": str(int(time.time() * 1000))}, timeout=40)
    if response.status_code != 200:
        return None, None
    data = response.json()
    for key in ["download", "dtoken", "httppath", "http"]:
        value = data.get(key)
        if isinstance(value, str) and value.startswith("http"):
            filename = data.get("filename") or data.get("name")
            return value, clean_text(filename) if filename else None
    return None, None


def ensure_extension(name: str, url: str) -> str:
    suffix = Path(urllib.parse.urlsplit(url).path).suffix.lower()
    if suffix in DOWNLOAD_EXTS and not Path(name).suffix:
        return f"{name}{suffix}"
    return name


def download_courseware(session: requests.Session, out_dir: Path, course_id: str, class_id: str, cpi: str) -> list[dict[str, Any]]:
    files_dir = out_dir / "courseware"
    files_dir.mkdir(parents=True, exist_ok=True)

    saved = []
    seen_objectids = set()
    chapters = chapter_items(session, course_id, class_id, cpi)
    for chapter in chapters:
        cards_url = "https://mooc1.chaoxing.com/mooc-ans/knowledge/cards"
        cards = session.get(
            cards_url,
            params={
                "clazzid": class_id,
                "courseid": course_id,
                "knowledgeid": chapter["knowledgeid"],
                "num": "0",
                "ut": "s",
                "cpi": cpi,
                "mooc2": "1",
            },
            timeout=40,
        )
        for attachment in extract_attachments_from_cards(cards.text):
            object_id = attachment["objectid"]
            if object_id in seen_objectids:
                continue
            seen_objectids.add(object_id)

            download_url, filename = resolve_download_url(session, object_id)
            if not download_url:
                continue
            raw_name = filename or attachment["name"] or f"{object_id}.bin"
            raw_name = ensure_extension(raw_name, download_url)
            ext = Path(raw_name).suffix.lower()
            if ext and ext not in DOWNLOAD_EXTS:
                continue
            safe_filename = safe_name(raw_name)
            target = files_dir / safe_filename

            with session.get(download_url, stream=True, timeout=120) as response:
                response.raise_for_status()
                with target.open("wb") as fh:
                    for chunk in response.iter_content(chunk_size=1024 * 128):
                        if chunk:
                            fh.write(chunk)

            saved.append(
                {
                    "chapter": chapter["title"],
                    "knowledgeid": chapter["knowledgeid"],
                    "objectid": object_id,
                    "filename": safe_filename,
                    "path": str(target),
                }
            )
    return saved


def build_docx(path: Path, title: str, questions: list[dict[str, Any]], include_answers: bool) -> None:
    def para(text: str = "", style: str | None = None) -> str:
        style_xml = f'<w:pPr><w:pStyle w:val="{style}"/></w:pPr>' if style else ""
        return f'<w:p>{style_xml}<w:r><w:t xml:space="preserve">{escape(text or "")}</w:t></w:r></w:p>'

    body = [para(title, "Title")]
    current = None
    for question in questions:
        group = f"{SOURCE_LABELS.get(question['source'], question['source'])} - {question['set']}"
        if group != current:
            body.append(para(group, "Heading1"))
            current = group
        body.append(para(f"{question['num']}. [{question['type']}] {question['stem']}"))
        for option in question.get("options") or []:
            body.append(para(f"    {option}"))
        if include_answers:
            answer = question.get("answer") or "未公开"
            source = ANSWER_SOURCE_LABELS.get(question.get("answer_source"), question.get("answer_source") or "未公开")
            body.append(para(f"答案：{answer}（来源：{source}）"))
            if question.get("analysis"):
                body.append(para(f"解析：{question['analysis']}"))
            if question.get("student_answer"):
                body.append(para(f"我的答案：{question['student_answer']}"))

    document = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body>'
        + "".join(body)
        + '<w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/></w:sectPr></w:body></w:document>'
    )
    styles = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        '<w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:rPr><w:b/><w:sz w:val="32"/></w:rPr></w:style>'
        '<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:rPr><w:b/><w:sz w:val="28"/></w:rPr></w:style></w:styles>'
    )
    content_types = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
        '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/></Types>'
    )
    rels = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>'
    doc_rels = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>'

    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("[Content_Types].xml", content_types)
        archive.writestr("_rels/.rels", rels)
        archive.writestr("word/_rels/document.xml.rels", doc_rels)
        archive.writestr("word/document.xml", document)
        archive.writestr("word/styles.xml", styles)


async def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cdp", default="http://127.0.0.1:9222")
    parser.add_argument("--out", default=".")
    parser.add_argument("--mode", choices=["questions", "courseware", "all"], default="all")
    parser.add_argument("--course-id")
    parser.add_argument("--class-id")
    parser.add_argument("--cpi")
    parser.add_argument("--fid", default="18078")
    args = parser.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    cdp = CDP(args.cdp)
    state = await cdp.course_state()
    params = query(state["href"])
    course_id = args.course_id or params.get("courseid") or params.get("courseId")
    class_id = args.class_id or params.get("clazzid") or params.get("classId")
    cpi = args.cpi or params.get("cpi")
    if not (course_id and class_id and cpi):
        raise RuntimeError("Could not infer course-id/class-id/cpi from the current course tab.")

    session = make_session(await cdp.cookies())

    questions = []
    if args.mode in {"questions", "all"}:
        homework_list_url = await cdp.homework_list_url()
        for work in parse_homework_list(session, course_id, class_id, cpi, homework_list_url):
            questions.extend(parse_homework_page(session, work, course_id, class_id, cpi))
        for activity in parse_activity_list(session, args.fid, course_id, class_id):
            questions.extend(parse_quiz(session, activity))
        (out / "chaoxing_questions_raw.json").write_text(json.dumps(questions, ensure_ascii=False, indent=2), encoding="utf-8")
        build_docx(out / "chaoxing_review_questions.docx", "学习通复习题目", questions, include_answers=False)
        build_docx(out / "chaoxing_review_answers.docx", "学习通复习答案", questions, include_answers=True)

    courseware = []
    if args.mode in {"courseware", "all"}:
        courseware = download_courseware(session, out, course_id, class_id, cpi)
        (out / "chaoxing_courseware_manifest.json").write_text(json.dumps(courseware, ensure_ascii=False, indent=2), encoding="utf-8")

    report = {
        "course_title": state.get("title"),
        "course_id": course_id,
        "class_id": class_id,
        "mode": args.mode,
        "total_questions": len(questions),
        "with_answers": sum(1 for item in questions if item.get("answer")),
        "without_answers": sum(1 for item in questions if not item.get("answer")),
        "courseware_downloaded": len(courseware),
        "outputs": [
            "chaoxing_export_report.json",
            "chaoxing_questions_raw.json",
            "chaoxing_review_questions.docx",
            "chaoxing_review_answers.docx",
            "chaoxing_courseware_manifest.json",
            "courseware/",
        ],
    }
    (out / "chaoxing_export_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
