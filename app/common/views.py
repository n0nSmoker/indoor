from flask import Blueprint, render_template, redirect

from lib.auth.manager import current_user


mod = Blueprint('common', __name__)


@mod.route('/')
@mod.route('/admin/<path:path>/')
def root_view(path=None):
    if not current_user:
        return redirect('/login/')
    # TODO: make it on front
    if not path:
        return redirect('/admin/users/')
    return render_template('index.html')


@mod.route('/login/')
def login_view():
    return render_template('login.html')


@mod.route('/heartbeat/')
def heartbeat_view():
    """Service availability check

    :return: ''
    """
    return ''
