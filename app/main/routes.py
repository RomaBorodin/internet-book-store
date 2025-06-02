from flask import render_template, redirect, url_for
from flask_login import current_user

from . import main_bp


@main_bp.route('/')
def home():
    if current_user.is_authenticated:
        return render_template('main/home.html')
    else:
        return render_template('main/index.html')
