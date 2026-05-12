# Chaoxing Endpoint Notes

Use these notes when `scripts/chaoxing_export.py` needs adjustment.

## Course Shell

- Main course page:
  `https://mooc2-ans.chaoxing.com/mooc2-ans/mycourse/stu?...`
- Chapter iframe:
  `#frame_content-zj`
- Homework iframe:
  `#frame_content-zy`
- Task/activity iframe:
  `#frame_content-hd`

## PPT And Document Attachments

1. Parse `.chapter_item` nodes in the chapter iframe.
2. Filter title text containing `璇句欢` or `PPT`.
3. Extract `knowledgeId` from `toOld(courseId, knowledgeId, clazzId, ...)`.
4. Request cards:
   `/mooc-ans/knowledge/cards?clazzid=<clazzid>&courseid=<courseid>&knowledgeid=<knowledgeId>&num=0&ut=s&cpi=<cpi>&mooc2=1`
5. Parse `<iframe module="insertdoc" data="...">` and `mArg.attachments`.
6. Resolve file metadata with `/ananas/status/<objectid>` from a `mooc1.chaoxing.com` page context if direct requests are blocked.

## Homework

1. Load `/mooc2/work/list?courseId=<courseId>&classId=<classId>&cpi=<cpi>&ut=s`.
2. Parse `li[onclick*=goTask]` and its `data` URL.
3. Request each task URL. If it redirects to `/work/prompt`, parse hidden:
   - `workId`
   - `answerId`
   - `enc`
   - `standardEnc`
4. Retry:
   `/mooc-ans/mooc2/work/view?courseId=<courseId>&classId=<classId>&cpi=<cpi>&workId=<workId>&answerId=<answerId>&standardEnc=<standardEnc>&enc=<enc>`
5. Parse `.questionLi`, `.mark_name`, `.qtDetail li`, `.stuAnswerContent`, `.rightAnswerContent`, and `.qtAnalysis`.

## In-Class Practice

1. Load activity list:
   `/v2/apis/active/student/activelist?fid=<fid>&courseId=<courseId>&classId=<classId>&showNotStartedActive=0`
2. Filter `activeType == 42`.
3. For each active id, try:
   `/v2/apis/studentQuestion/getAnswerResult?activeId=<activeId>`
4. Fall back to:
   `/v2/apis/quiz/quizDetail2?activeId=<activeId>&moreClassAttendEnc=&DB_STRATEGY=PRIMARY_KEY&STRATEGY_PARA=activeId`
5. Parse `questionList` or `questionlist`, `answer`, and `personAnswer`.

## Common Failures

- `403 rejected ip`: retry through the logged-in browser context or disable proxy environment inheritance for plain metadata requests.
- Empty iframe body: use Chrome DevTools Protocol `Page.getFrameTree` and `Page.createIsolatedWorld`.
- Garbled Chinese in PowerShell output: set `PYTHONIOENCODING=utf-8`.
- Direct homework view has zero questions: retry with `standardEnc`.
