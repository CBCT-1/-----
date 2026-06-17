---
name: chaoxing-course-export-v1-2
description: Export authorized Chaoxing/Xuexitong course materials for review, version 1.2. Use when Codex needs to download PPT/PDF courseware, collect completed homework, in-class practice, and completed “我的考试” exam questions with visible answers, handle updated homework iframes carrying stuenc/enc parameters, and generate local DOCX/JSON review files from a logged-in browser session.
---

# Chaoxing Course Export v1.2

Use this skill to help a user archive their own Chaoxing/Xuexitong course resources into local study files.

This is a separate v1.2 skill and should not overwrite `chaoxing-course-export` or `chaoxing-course-export-v1-1`.

## Safety Boundary

- Work only from a browser session the user has already logged into and authorized.
- Download inbound course files only; never transmit account credentials.
- Do not bypass access controls. If a page or API does not expose answers, record `未公开`.
- For active or ongoing quizzes or exams, collect visible questions for review only. Do not provide direct answers intended for live submission.
- For completed practice where answers are unpublished, you may add model-generated study explanations only if the user explicitly asks for review help; label them as `模型推断` rather than `学习通答案`.
- Remove temporary HTML, cookie dumps, and debug files. Keep final DOCX/JSON outputs only.

## Preferred Workflow

1. Confirm the user has opened the target course in Edge or Chrome and is logged in.
2. If the browser is not controllable, launch a temporary profile with remote debugging:
   - Edge: `msedge.exe --remote-debugging-port=9222 --user-data-dir=<temp-profile> <course-url>`
   - Ask the user to log in inside that temporary window.
3. Use `scripts/chaoxing_export.py` from this skill when possible:
   - `python scripts/chaoxing_export.py --out <output-dir> --mode all`
   - For only completed exams: `python scripts/chaoxing_export.py --out <output-dir> --mode exams`
   - Add `--cdp http://127.0.0.1:9222` when using a custom debugging port.
   - For homework, prefer the real `#frame_content-zy` iframe URL from the logged-in course page. Updated Chaoxing pages may require `stuenc` and `enc`; the script loads/clicks the homework tab through CDP before requesting `/mooc2/work/list`.
   - For exams, open the course’s `考试 -> 我的考试` page or let the script find the `/exam-ans/exam/test` link from the course shell. The script follows each completed `查看` link and parses the authorized review page.
4. Inspect the generated report:
   - `chaoxing_export_report.json`
   - `chaoxing_questions_raw.json`
   - `chaoxing_review_questions.docx`
   - `chaoxing_review_answers.docx`
   - `chaoxing_exam_questions_raw.json`
   - `chaoxing_exam_questions.docx`
   - `chaoxing_exam_answers.docx`
5. If the script misses a page, read [references/chaoxing-endpoints.md](references/chaoxing-endpoints.md), inspect the iframe URL and page scripts, then patch or rerun with the discovered URL.

## Implementation Notes

- The course shell usually lives on `mooc2-ans.chaoxing.com/mooc2-ans/mycourse/stu`.
- Chapter content is usually inside `#frame_content-zj`; PPT/doc attachments are in `/mooc-ans/knowledge/cards`.
- Homework is usually inside `frame_content-zy` and `/mooc2/work/list`.
- Updated homework pages may reject a plain `/mooc2/work/list?courseId=...&classId=...&cpi=...` request with `无权限的操作`. Use the iframe URL containing `stuenc` and `enc`.
- In-class practice is usually under `mobilelearn.chaoxing.com/page/active/stuActiveList`.
- Completed exams are usually listed at `/exam-ans/exam/test?...` under `考试 -> 我的考试`; each completed item has a `查看` link to `/exam-ans/exam/test/reVersionPaperMarkContentNew?...&id=<exam-id>&cpi=<cpi>`.
- Some homework pages first show a prompt. If `standardEnc` is present, retry `/mooc2/work/view` with `standardEnc`.
- Some download URLs reject non-browser requests. Prefer letting the controlled browser perform downloads, or use status endpoints only to resolve filenames and metadata.

## Output Expectations

- Name files by course/task title and keep Chinese titles intact.
- Produce one question-only DOCX and one answer DOCX.
- For completed exams, produce separate exam question and answer DOCX files in addition to the homework/practice files.
- Use Chinese question type labels in documents and JSON, such as `单选题`, `多选题`, `填空题`, `判断题`, `简答题`, `名词解释`, `论述题`, and `计算题`.
- For `判断题`, normalize options and answers to `对`/`错`; do not leave them as `1`/`2`, `true`/`false`, or `A`/`B`.
- Include source labels for answers:
  - `学习通答案`: answer was visible in Chaoxing/Xuexitong.
  - `未公开`: no answer was exposed.
  - `模型推断`: answer was generated for study after the user asked for it.
- Keep a raw JSON file so the user can regenerate documents without scraping again.
