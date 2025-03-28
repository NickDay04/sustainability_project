# -*- coding: utf-8 -*-
"""
    main/views.py
    ~~~~~~~~~~~~~

    Contains routing and rendering for all home pages.

    :copyright: (c) 2024 by Newcastle University CSC2033 Team 8.
    :license: see LICENSE.MD for more details.
"""

from flask import Blueprint, render_template
from flask_login import login_user

from models import User

index_blueprint = Blueprint('index', __name__, template_folder='templates')


@index_blueprint.route('/')
def index():
    # user = User.query.filter(User.id == 1).first()
    # login_user(user)
    return render_template('main/index.html', user="meow")
