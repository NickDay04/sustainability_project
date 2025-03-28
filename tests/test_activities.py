from datetime import datetime
from flask import session


'''
Test ID: WB04
'''
def test_status_code(client):
    response = client.get("/activities/")
    assert response.status_code == 200


'''
Test ID: WB05
'''
def test_home(client):
    response = client.get("/activities/")
    html = response.data.decode("utf-8").replace(" ", "")
    assert '<ahref="/activities/add_activity">\n<button><iclass="fa-solidfa-plus"></i>&nbsp;AddActivity</button>\n</a>' in html
    assert '<ahref="/activities/activity_history?active=graph">\n<button><iclass="fa-solidfa-clock-rotate-left"></i>&nbsp;ViewActivityHistory</button>\n</a>' in html
    assert '<ahref="/activities/resources">\n<button><iclass="fa-solidfa-sitemap"></i>&nbsp;Resources</button>\n</a>' in html
    assert '<ahref="/activities/activity_analysis?time_frame=7">\n<button><iclass="fa-solidfa-chart-pie"></i>&nbsp;ActivityAnalysis</button>\n</a>' in html

