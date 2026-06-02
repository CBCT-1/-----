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
2. Filter title text containing `课件` or `PPT` when the user only wants courseware; otherwise scan every chapter.
3. Extract `knowledgeId` from `toOld(courseId, knowledgeId, clazzId, ...)`. Newer pages may quote arguments, e.g. `toOld('260477255', '1110219598', '139139199',0)`.
4. Request cards:
   `/mooc-ans/knowledge/cards?clazzid=<clazzid>&courseid=<courseid>&knowledgeid=<knowledgeId>&num=0&ut=s&cpi=<cpi>&mooc2=1`
5. Parse `<iframe module="insertdoc" data="...">` and `mArg.attachments`. The `data` value is often HTML-escaped JSON and should be decoded before `json.loads`.
6. Resolve file metadata with `/ananas/status/<objectid>` from a `mooc1.chaoxing.com` page context if direct requests are blocked.

## Homework

1. Prefer the live `#frame_content-zy` iframe `src` from the logged-in course page. Current pages may include required `stuenc` and `enc` parameters:
   `/mooc2/work/list?courseId=<courseId>&classId=<classId>&cpi=<cpi>&ut=s&t=<ts>&stuenc=<course-enc>&enc=<work-enc>`.
2. If `#frame_content-zy` is not present, click/load the homework nav (`li[dataname="zy"] a[data-url]`) through CDP and wait for the iframe.
3. Use the plain `/mooc2/work/list?courseId=<courseId>&classId=<classId>&cpi=<cpi>&ut=s` URL only as fallback; it may return `无权限的操作`.
4. Parse `li[onclick*=goTask]` and its `data` URL.
5. Request each task URL. If it redirects to `/work/prompt`, parse hidden:
   - `workId`
   - `answerId`
   - `enc`
   - `standardEnc`
6. Retry:
   `/mooc-ans/mooc2/work/view?courseId=<courseId>&classId=<classId>&cpi=<cpi>&workId=<workId>&answerId=<answerId>&standardEnc=<standardEnc>&enc=<enc>`
7. Parse `.questionLi`, `.mark_name`, `.qtDetail li`, `.stuAnswerContent`, `.rightAnswerContent`, and `.qtAnalysis`.
8. Normalize question type labels to Chinese. For `判断题`, normalize options and answers to `对`/`错` instead of `1`/`2` or `A`/`B`.

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
