from flask import Blueprint, request
from start.response import make_succ_empty_response, make_succ_response, make_err_response

from user import user_app


@user_app.route('/')
def get_user():

    openid = request.headers.get('x-wx-openid')
    source = request.headers.get('x-wx-source')

    data = {'headers': request.headers}
    return make_succ_response(f'测试{request.args}; data={data}')