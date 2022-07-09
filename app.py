from multipage import MultiPage
from pages import project, project1, project2

app = MultiPage()

app.add_page("Project", project.app)
app.add_page("따릉이 대여소 지도", project1.app)
app.add_page("기온 데이터 분석", project2.app)

app.run()