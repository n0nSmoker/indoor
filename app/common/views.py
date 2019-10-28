from flask import Blueprint


mod = Blueprint('common', __name__)


@mod.route('/')
def root_view():
    return 'Main page'


@mod.route('/heartbeat/')
def heartbeat_view():
    """Service availability check

    :return: ''
    """
    return ''
