---
name: chaoxing-course-export
description: Export authorized Chaoxing/Xuexitong course materials for review. Use when Codex needs to download PPT/PDF courseware from chapter pages, collect completed or visible homework and in-class practice questions, extract published answers, and generate local review DOCX/JSON files from a logged-in browser session.
---

# Chaoxing Course Export

Use this skill to help a user archive their own Chaoxing/Xuexitong course resources into local study files.

## Safety Boundary

- Work only from a browser session the user has already logged into and authorized.
- Download inbound course files only; never transmit account credentials.
- Do not bypass access controls. If a page or API does not expose answers, record `鏈叕甯僠.
- For active or ongoing quizzes, collect visible questions for review only. Do not provide direct answers intended for live submission.
- For completed practice where answers are unpublished, you may add model-generated study explanations only if the user explicitly asks for review help; label them as `妯″瀷鎺ㄦ柇` rather than `瀛︿範閫氱瓟妗坄.
- Remove temporary HTML, cookie dumps, and debug files. Keep final DOCX/JSON outputs only.

## Preferred Workflow

1. Confirm the user has opened the target course in Edge or Chrome and is logged in.
2. If the browser is not controllable, launch a temporary profile with remote debugging:
   - Edge: `msedge.exe --remote-debugging-port=9222 --user-data-dir=<temp-profile> <course-url>`
   - Ask the user to log in inside that temporary window.
3. Use `scripts/chaoxing_export.py` from this skill when possible:
   - `python scripts/chaoxing_export.py --out <output-dir> --mode all`
   - Add `--cdp http://127.0.0.1:9222` when using a custom debugging port.
4. Inspect the generated report:
   - `chaoxing_export_report.json`
   - `chaoxing_questions_raw.json`
   - `chaoxing_review_questions.docx`
   - `chaoxing_review_answers.docx`
5. If the script misses a page, read [references/chaoxing-endpoints.md](references/chaoxing-endpoints.md), inspect the iframe URL and page scripts, then patch or rerun with the discovered URL.

## Implementation Notes

- The course shell usually lives on `mooc2-ans.chaoxing.com/mooc2-ans/mycourse/stu`.
- Chapter content is usually inside `#frame_content-zj`; PPT/doc attachments are in `/mooc-ans/knowledge/cards`.
- Homework is usually inside `frame_content-zy` and `/mooc2/work/list`.
- In-class practice is usually under `mobilelearn.chaoxing.com/page/active/stuActiveList`.
- Some homework pages first show a prompt. If `standardEnc` is present, retry `/mooc2/work/view` with `standardEnc`.
- Some download URLs reject non-browser requests. Prefer letting the controlled browser perform downloads, or use status endpoints only to resolve filenames and metadata.

## Output Expectations

- Name files by course/task title and keep Chinese titles intact.
- Produce one question-only DOCX and one answer DOCX.
- Include source labels for answers:
  - `瀛︿範閫歚: answer was visible in Chaoxing/Xuexitong.
  - `鏈叕甯僠: no answer was exposed.
  - `妯″瀷鎺ㄦ柇`: answer was generated for study after the user asked for it.
- Keep a raw JSON file so the user can regenerate documents without scraping again.
