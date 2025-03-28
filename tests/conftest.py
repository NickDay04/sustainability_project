import pytest 
import os

from dotenv import load_dotenv

from flask_login import login_user

from app import create_app
from models import User

load_dotenv()


def login_default_user():
    user = User.query.filter_by(role="user").first()
    assert user.role == "user"
    login_user(user)
    return user


def login_admin_user():
    admin = User.query.filter_by(email="admin@email.com").first()
    assert admin.role == "admin"
    login_user(admin)


@pytest.fixture(scope="module")
def client():
    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "mysql+pymysql://" \
                + os.getenv("MYSQL_USER") \
                + ":" \
                + os.getenv("MYSQL_PASSWORD") \
                + "@" \
                + os.getenv("MYSQL_HOST") \
                + "/dev",
            "WTF_CSRF_ENABLED": False,
            "LOGIN_DISABLED": True
        })
    with app.test_client() as client:
        yield client