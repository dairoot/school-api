from school_api.client.api.base import BaseSchoolApi
from bs4 import BeautifulSoup


class Score(BaseSchoolApi):

    def get_score(self, **kwargs):
        score_url = self.school_url['SCORE_URL'] + self.account
        view_state = self._get_view_state(score_url)
        payload = {
            '__VIEWSTATE': view_state,
            'Button2': u'在校学习成绩查询',
            'ddlXN': '',
            'ddlXQ': ''
        }
        res = self._post(score_url, data=payload)
        if res.status_code != 200:
            return None
        soup = BeautifulSoup(res.content.decode('GB18030'), "html.parser")
        rows = soup.find("table", {"id": "Datagrid1"}).find_all('tr')
        # 弹出第一行列名
        rows.pop(0)
        # 访问查询全部成绩页面，提取当前学年学期的成绩
        score_info = []
        for row in rows:
            cells = row.find_all("td")
            # 学年学期
            year = cells[0].text
            term = cells[1].text
            # 课程名
            lesson_name = cells[3].text.strip()
            # 学分：
            credit = cells[6].text.strip() or 0
            # 绩点
            point = cells[7].text.strip() or 0
            # 最终成绩
            score = cells[8].text.strip() or 0
            # 组装文本格式数据回复用户
            score_dict = {
                "lesson_name": lesson_name,
                "credit": float(credit),
                "point": float(point),
                "score": float(score),
                "year": year,
                "term": int(term)
            }
            # 有其他成绩内容则输出
            makeup_score = cells[10].text
            retake_score = cells[11].text
            if makeup_score != u'\xa0':
                # 补考成绩
                score_dict['bkcj'] = makeup_score
            if retake_score != u'\xa0':
                # 重修成绩
                score_dict['cxcj'] = retake_score
            # 组装数组格式的数据备用
            score_info.append(score_dict)
        return score_info
