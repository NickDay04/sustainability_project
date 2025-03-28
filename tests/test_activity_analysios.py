from flask import render_template
import pytest
from tests.conftest import login_default_user
from app import app


@pytest.fixture
def app_context():
    with app.app_context():
        yield


'''
WB15
Tests that activity analysis can change time span it is analysed over.
'''
def test_buttons(client):
    client.get("/")
    login_default_user()
    html = render_template("/activities/activity_analysis.html", motor_result=0, flight_result=0, food_result=0)
    assert '<button>7 Days</button>' in html
    assert '<button>14 Days</button>' in html
    assert '<button>1 Month</button>' in html
    assert '<button>3 Months</button>' in html
    assert '<button>6 Months</button>' in html
    assert '<button>1 Year</button>' in html


'''
WB16
Tests the three categories that are analysed are present.
'''
def test_headers(client):
    client.get("/")
    login_default_user()
    html = render_template("/activities/activity_analysis.html", motor_result=0, flight_result=0, food_result=0)
    assert '<h1 class="roboto-light-500">Cars, Vans, Motorbikes</h1>' in html
    assert '<h1 class="roboto-light-500">Flights</h1>' in html
    assert '<h1 class="roboto-light-500">Food</h1>'


'''
WB17
Tests that activity analysis compares activity to national averages
'''
def test_colors(client):
    client.get("/")
    login_default_user()
    html = render_template("/activities/activity_analysis.html", motor_result=100, flight_result=0, food_result=200)
    assert "<div class='block   green'>" in html
    assert "<div class='block  orange '>" in html
    assert "<div class='block red  '>" in html