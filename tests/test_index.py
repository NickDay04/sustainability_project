import pytest

from flask import render_template
from flask_login import login_user

from models import User
from app import app
from tests.conftest import login_default_user, login_admin_user


@pytest.fixture
def app_context():
    with app.app_context():
        yield


'''
Test ID: WB02
'''
def test_status_code(client):
    response = client.get("/")
    assert response.status_code == 200


'''
Test ID: WB01
'''
def test_anonymous_home_page(client):
    response = client.get("/")
    html = response.data.decode("utf-8").replace(" ", "")
    assert '<ahref="/login">\n<button>Login</button>\n</a>' in html
    assert '<ahref="/register">\n<button>Register</button>\n</a>' in html


'''
Test ID: WB03
'''
def test_loggedin_home_page(client):
    login_default_user()
    html = render_template("main/index.html").replace(" ", "")
    assert '<ahref="/activities">\n<button>Activities</button>\n</a>' in html
    assert '<ahref="/account">\n<button>Account</button>\n</a>' in html
    assert '<ahref="/social/feed">\n<button>SocialMedia</button>\n</a>' in html
    assert '<ahref="/logout">\n<button>Logout</button>\n</a>' in html
