import importlib.util
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "chaoxing-course-export-v1-2" / "scripts" / "chaoxing_export.py"


def load_exporter():
    spec = importlib.util.spec_from_file_location("chaoxing_export_v1_2", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ExamExportTests(unittest.TestCase):
    def test_parse_exam_list_finds_completed_exam_view_links(self):
        exporter = load_exporter()
        html = """
        <ul>
          <li class="lookLi">
            <div class="titTxt"><a>绪论</a> 考试时间： 2026-06-04 15:08 至 2026-06-07 23:55 考试状态： 已完成</div>
            <div class="titOper">90分 <a class="Btn_blue_1" onclick="location.href='/exam-ans/exam/test/reVersionPaperMarkContentNew?courseId=260477255&amp;classId=139139199&amp;p=1&amp;id=169645752&amp;ut=s&amp;examsystem=0&amp;cpi=424627627';">查看</a></div>
          </li>
          <li class="lookLi">
            <div class="titTxt"><a>RNA转录</a> 考试时间： 2026-05-27 14:31 至 2026-05-31 23:32 考试状态： 已完成</div>
            <div class="titOper">88分 <a class="Btn_blue_1" onclick="location.href='/exam-ans/exam/test/reVersionPaperMarkContentNew?courseId=260477255&amp;classId=139139199&amp;p=1&amp;id=169522547&amp;ut=s&amp;examsystem=0&amp;cpi=424627627';">查看</a></div>
          </li>
        </ul>
        """

        exams = exporter.parse_exam_list_html(html, "https://mooc1-2.chaoxing.com/exam-ans/exam/test")

        self.assertEqual([exam["title"] for exam in exams], ["绪论", "RNA转录"])
        self.assertEqual(exams[0]["score"], "90")
        self.assertEqual(exams[0]["exam_id"], "169645752")
        self.assertTrue(exams[0]["url"].startswith("https://mooc1-2.chaoxing.com/exam-ans/exam/test/reVersionPaperMarkContentNew"))
        self.assertNotIn("amp;", exams[0]["url"])

    def test_parse_exam_detail_normalizes_single_choice_and_true_false(self):
        exporter = load_exporter()
        html = """
        <html><body>
          <div class="TiMu">
            <div class="Cy_TItle clearfix"><i class="fl">1</i><div class="fl clearfix">第一个重组DNA分子是在哪一年构建成功的?（&nbsp;&nbsp;）（5.0分）</div></div>
            <ul class="Cy_ulTop"><form>
              <input name="type" value="0"/><input name="score" value="5.0"/><input name="myanswer" value="C"/><input name="qid" value="q1"/>
              <li><i class="fl">A、</i><div class="clearfix"><a>Avery</a></div></li>
              <li><i class="fl">B、</i><div class="clearfix"><a>Beadle 和 Tatum</a></div></li>
              <li><i class="fl">C、</i><div class="clearfix"><a>1972年</a></div></li>
              <li><i class="fl">D、</i><div class="clearfix"><a>1980年</a></div></li>
            </form></ul>
            <div class="Py_answer clearfix"><span>正确答案： C</span><span>我的答案：C</span></div>
          </div>
          <div class="TiMu">
            <div class="Cy_TItle clearfix"><i class="fl">2</i><div class="fl clearfix">目前已知自然界中所有生物的遗传物质都是DNA。（ ）（5.0分）</div></div>
            <form><input name="type" value="3"/><input name="score" value="5.0"/><input name="myanswer" value="false"/><input name="qid" value="q2"/></form>
            <div class="Py_answer clearfix"><span>正确答案：<i>×</i></span><span>我的答案：<i>×</i></span></div>
          </div>
        </body></html>
        """

        parsed = exporter.parse_exam_detail_html(html, {"title": "绪论"})

        self.assertEqual(parsed["question_count"], 2)
        first, second = parsed["questions"]
        self.assertEqual(first["type"], "单选题")
        self.assertEqual(first["stem"], "第一个重组DNA分子是在哪一年构建成功的?（ ）")
        self.assertEqual(
            first["options"],
            [
                {"label": "A", "text": "Avery"},
                {"label": "B", "text": "Beadle 和 Tatum"},
                {"label": "C", "text": "1972年"},
                {"label": "D", "text": "1980年"},
            ],
        )
        self.assertEqual(first["answer"], "C")
        self.assertEqual(second["type"], "判断题")
        self.assertEqual(second["options"], [{"label": "A", "text": "对"}, {"label": "B", "text": "错"}])
        self.assertEqual(second["answer"], "错")
        self.assertEqual(second["student_answer"], "错")


if __name__ == "__main__":
    unittest.main()
