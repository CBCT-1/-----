#!/usr/bin/env python3
"""
Export authorized Chaoxing/Xuexitong courseware and review questions from a
logged-in Chromium/Edge session exposed through Chrome DevTools Protocol.

This script is intentionally conservative: it records unpublished answers as
未公布 and never attempts to submit or modify coursework.
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
    18: "口头题",
}


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


class CDP:
    def __init__(self, cdp_base: str):
        self.cdp_base = cdp_base.rstrip("/")
        self._idx = 0

    def tabs(self) -> list[dict[str, Any]]:
        with urllib.request.urlopen(f"{self.cdp_base}/json/list") as r:
            return json.load(r)

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
                    "expression": """(()=>({\n                        href: location.href,\n                        title: document.title,\n                        frames: Array.from(document.querySelectorAll('iframe,frame')).map(f=>({id:f.id,name:f.name,src:f.src}))\n                    }))()""",
                    "returnByValue": True,
                    "awaitPromise": True,
                },
            )
            return result["result"]["result"]["value"]


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


def parse_homework_list(session: requests.Session, course_id: str, class_id: str, cpi: str) -> list[dict[str, str]]:
    url = f"https://mooc1.chaoxing.com/mooc2/work/list?courseId={course_id}&classId={class_id}&cpi={cpi}&ut=s&t={int(time.time()*1000)}"
    soup = BeautifulSoup(session.get(url, timeout=40).text, "html.parser")
    works = []
    for li in soup.select('li[onclick*="goTask"]'):
        task_url = html.unescape(li.get("data") or "")
        name = clean_text((li.select_one(".right-content p:first-child") or li).get_text(" "))
        status_el = li.select_one("p.status")
        works.append({"source": "作业", "name": name, "status": clean_text(status_el.get_text(" ")) if status_el else "", "url": task_url})
    return [w for w in works if w["url"]]


def parse_homework_page(session: requests.Session, work: dict[str, str], course_id: str, class_id: str, cpi: str) -> list[dict[str, Any]]:
    response = session.get(work["url"], timeout=40, allow_redirects=True)
    soup = BeautifulSoup(response.text, "html.parser")
    if not soup.select(".questionLi"):
        ids = {key: (soup.select_one(f"#{key}") or {}).get("value") for key in ["workId", "answerId", "enc", "standardEnc"]}
        if all(ids.values()):
            retry = (
                "https://mooc1.chaoxing.com/mooc-ans/mooc2/work/view"
                f"?courseId={course_id}&classId={class_id}&cpi={cpi}&workId={ids['workId']}"
                f"&answerId={ids['answerId']}&standardEnc={ids['standardEnc']}&enc={ids['enc']}"
            )
            soup = BeautifulSoup(session.get(retry, timeout=40).text, "html.parser")

    title_el = soup.select_one(".mark_title") or soup.select_one("h2")
    title = clean_text(title_el.get_text(" ")) if title_el else work["name"]
    questions = []
    for q in soup.select(".questionLi"):
        name_el = q.select_one(".mark_name")
        raw = clean_text(name_el.get_text(" ", strip=True)) if name_el else ""
        match = re.match(r"^(\d+)\.\s*(?:\(([^)（]+)[)）])?\s*(.*)$", raw, flags=re.S)
        num = match.group(1) if match else str(len(questions) + 1)
        qtype = match.group(2) if match and match.group(2) else ""
        stem = match.group(3).strip() if match else raw
        questions.append(
            {
                "source": "作业",
                "set": title,
                "status": work.get("status", ""),
                "num": num,
                "type": qtype,
                "stem": stem,
                "options": [clean_text(li.get_text(" ", strip=True)) for li in q.select(".qtDetail li")],
                "student_answer": clean_text(q.select_one(".stuAnswerContent").get_text(" ", strip=True)) if q.select_one(".stuAnswerContent") else "",
                "answer": clean_text(q.select_one(".rightAnswerContent").get_text(" ", strip=True)) if q.select_one(".rightAnswerContent") else "",
                "analysis": clean_text(q.select_one(".qtAnalysis").get_text(" ", strip=True)) if q.select_one(".qtAnalysis") else "",
            }
        )
    for q in questions:
        q["answer_source"] = "学习通" if q["answer"] else "未公布"
    return questions


def parse_activity_list(session: requests.Session, fid: str, course_id: str, class_id: str) -> list[dict[str, str]]:
    url = "https://mobilelearn.chaoxing.com/v2/apis/active/student/activelist"
    data = session.get(
        url,
        params={"fid": fid, "courseId": course_id, "classId": class_id, "showNotStartedActive": "0"},
        timeout=40,
    ).json()["data"]["activeList"]
    return [
        {"source": "随堂练习", "name": a.get("nameOne") or f"随堂练习 {a.get('id')}", "status": str(a.get("status")), "id": str(a.get("id"))}
        for a in data
        if str(a.get("activeType")) == "42"
    ]


def answer_from_quiz_question(q: dict[str, Any]) -> str:
    for key in ["rightAnswer", "answerStr", "answerResult", "standardAnswer", "correctAnswer", "answerContent"]:
        if q.get(key) not in [None, "", []]:
            return clean_text(q.get(key))
    letters = []
    for option in q.get("answer") or []:
        if option.get("isanswer") in [1, "1", True] or option.get("isRight") in [1, "1", True] or option.get("right") in [1, "1", True]:
            letters.append(clean_text(option.get("name")))
    return "".join(letters)


def student_quiz_answer(q: dict[str, Any]) -> str:
    person = q.get("personAnswer") or {}
    if person.get("myoption") not in [None, ""]:
        return clean_text(person.get("myoption"))
    if person.get("blankAnswer"):
        return "; ".join(f"{clean_text(x.get('name'))}:{clean_text(x.get('content'))}" for x in person.get("blankAnswer") or [])
    return clean_text(person.get("content"))


def parse_quiz(session: requests.Session, activity: dict[str, str]) -> list[dict[str, Any]]:
    result = session.get("https://mobilelearn.chaoxing.com/v2/apis/studentQuestion/getAnswerResult", params={"activeId": activity["id"]}, timeout=40).json()
    if result.get("result") != 1:
        result = session.get(
            "https://mobilelearn.chaoxing.com/v2/apis/quiz/quizDetail2",
            params={"activeId": activity["id"], "moreClassAttendEnc": "", "DB_STRATEGY": "PRIMARY_KEY", "STRATEGY_PARA": "activeId"},
            timeout=40,
        ).json()
    data = result.get("data") or {}
    qlist = data.get("questionList") or data.get("questionlist") or []
    active = data.get("active") or data.get("pptActive") or {}
    title = active.get("name") or activity["name"]
    questions = []
    for idx, q in enumerate(qlist, 1):
        answer = answer_from_quiz_question(q)
        questions.append(
            {
                "source": "随堂练习",
                "set": title,
                "status": "进行中" if activity.get("status") == "1" else "已结束",
                "num": str(idx),
                "type": TYPE_MAP.get(q.get("type"), f"题型{q.get('type')}"),
                "stem": clean_text(q.get("content")),
                "options": [
                    f"{clean_text(o.get('name'))}. {clean_text(o.get('content'))}".strip()
                    for o in q.get("answer") or []
                    if clean_text(o.get("name")) or clean_text(o.get("content"))
                ],
                "student_answer": student_quiz_answer(q),
                "answer": answer,
                "analysis": clean_text(q.get("analysis") or q.get("answerAnalysis") or q.get("resolve")),
                "answer_source": "学习通" if answer else "未公布",
            }
        )
    return questions


def build_docx(path: Path, title: str, questions: list[dict[str, Any]], include_answers: bool) -> None:
    def para(text: str = "", style: str | None = None) -> str:
        style_xml = f'<w:pPr><w:pStyle w:val="{style}"/></w:pPr>' if style else ""
        return f'<w:p>{style_xml}<w:r><w:t xml:space="preserve">{escape(text or "")}</w:t></w:r></w:p>'

    body = [para(title, "Title")]
    current = None
    for q in questions:
        group = f"{q['source']} - {q['set']}"
        if group != current:
            body.append(para(group, "Heading1"))
            current = group
        body.append(para(f"{q['num']}. [{q['type']}] {q['stem']}"))
        for option in q.get("options") or []:
            body.append(para(f"    {option}"))
        if include_answers:
            body.append(para(f"答案：{q.get('answer') or '未公布'}（来源：{q.get('answer_source') or '未公布'}）"))
            if q.get("analysis"):
                body.append(para(f"解析：{q['analysis']}"))
            if q.get("student_answer"):
                body.append(para(f"我的答案：{q['student_answer']}"))

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
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types)
        z.writestr("_rels/.rels", rels)
        z.writestr("word/_rels/document.xml.rels", doc_rels)
        z.writestr("word/document.xml", document)
        z.writestr("word/styles.xml", styles)


async def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cdp", default="http://127.0.0.1:9222")
    parser.add_argument("--out", default=".")
    parser.add_argument("--mode", choices=["questions", "all"], default="questions")
    parser.add_argument("--course-id")
    parser.add_argument("--class-id")
    parser.add_argument("--cpi")
    parser.add_argument("--fid", default="18078")
    args = parser.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    cdp = CDP(args.cdp)
    state = await cdp.course_state()
    q = query(state["href"])
    course_id = args.course_id or q.get("courseid") or q.get("courseId")
    class_id = args.class_id or q.get("clazzid") or q.get("classId")
    cpi = args.cpi or q.get("cpi")
    if not (course_id and class_id and cpi):
        raise RuntimeError("Could not infer course-id, class-id, and cpi from the active course tab.")

    session = make_session(await cdp.cookies())
    questions = []
    for work in parse_homework_list(session, course_id, class_id, cpi):
        questions.extend(parse_homework_page(session, work, course_id, class_id, cpi))
    for activity in parse_activity_list(session, args.fid, course_id, class_id):
        questions.extend(parse_quiz(session, activity))

    (out / "chaoxing_questions_raw.json").write_text(json.dumps(questions, ensure_ascii=False, indent=2), encoding="utf-8")
    build_docx(out / "chaoxing_review_questions.docx", "学习通期末复习题", questions, include_answers=False)
    build_docx(out / "chaoxing_review_answers.docx", "学习通期末复习题答案", questions, include_answers=True)
    report = {
        "course_title": state.get("title"),
        "course_id": course_id,
        "class_id": class_id,
        "total_questions": len(questions),
        "with_answers": sum(1 for item in questions if item.get("answer")),
        "without_answers": sum(1 for item in questions if not item.get("answer")),
        "outputs": ["chaoxing_questions_raw.json", "chaoxing_review_questions.docx", "chaoxing_review_answers.docx"],
    }
    (out / "chaoxing_export_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
