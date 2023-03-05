from flask import Blueprint, request
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response


user_app = Blueprint('user', __name__, url_prefix='/user')


@user_app.route('/')
def get_user():
    return make_succ_response(f'测试{request.args}')