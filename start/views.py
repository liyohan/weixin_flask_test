from datetime import datetime
from flask import render_template, request, make_response, redirect
from run import app
from start.dao import delete_counterbyid, query_counterbyid, insert_counter, update_counterbyid
from start.model import Counters
from start.response import make_succ_empty_response, make_succ_response, make_err_response

from urllib import parse
from start.middlewares import token_decode
import logging
import time
import config

logger = logging.getLogger('log')

#
# @app.route('/')
# def index():
#     """
#     :return: 返回index页面
#     """
#     return render_template('index.html')
#
#
# @app.route('/api/count', methods=['POST'])
# def count():
#     """
#     :return:计数结果/清除结果
#     """
#
#     # 获取请求体参数
#     params = request.get_json()
#
#     # 检查action参数
#     if 'action' not in params:
#         return make_err_response('缺少action参数')
#
#     # 按照不同的action的值，进行不同的操作
#     action = params['action']
#
#     # 执行自增操作
#     if action == 'inc':
#         counter = query_counterbyid(1)
#         if counter is None:
#             counter = Counters()
#             counter.id = 1
#             counter.count = 1
#             counter.created_at = datetime.now()
#             counter.updated_at = datetime.now()
#             insert_counter(counter)
#         else:
#             counter.id = 1
#             counter.count += 1
#             counter.updated_at = datetime.now()
#             update_counterbyid(counter)
#         return make_succ_response(counter.count)
#
#     # 执行清0操作
#     elif action == 'clear':
#         delete_counterbyid(1)
#         return make_succ_empty_response()
#
#     # action参数错误
#     else:
#         return make_err_response('action参数错误')
#
#
# @app.route('/api/count', methods=['GET'])
# def get_count():
#     """
#     :return: 计数的值
#     """
#     counter = Counters.query.filter(Counters.id == 1).first()
#     return make_succ_response(0) if counter is None else make_succ_response(counter.count)


def login():
    """
    拼接授权url地址
    """
    logger.error('获取授权地址')
    # 返回获取access_token地址
    REDIRECT_URI = parse.quote_plus(f'https://{request.host}/user/get_access_token/')
    url = f'https://open.weixin.qq.com/connect/oauth2/authorize?appid={config.app_id}&redirect_uri={REDIRECT_URI}&response_type=code&scope={config.scope}&state=1&#wechat_redirect'
    logger.error(url)

    return url


@app.route('/home/')
def home():
    logger.error('进入主页')
    res = make_response(render_template('home.html',
                                        open_url=login(),
                                        user_url=f'/wx/get_all_user/',
                                        work_url=f'/goods/get_data/'))
    res.headers['Content-Type'] = 'html'
    return res



@app.before_request
def before_request():
    """
    每次访问前判断
    1.用户是否带有token
    2.token解析是否正常，异常或超出时间限制时
    3.若不存在则进入授权界面，并赋予token
    :return:
    """

    logger.error('进入中间件判断')
    token = request.headers.get('token')
    logger.error(f'token: {token}')
    logger.error(f'uri: {request.url_rule}')

    try:
        # 获取token数据
        if str(request.url_rule) in ['/wx/', '/user/get_access_token/', '/favicon.ico']:
            # 当符合条件时忽略
            pass
        elif token:

            jwt_decode = token_decode(token)
            if not jwt_decode:  # 解析token失败
                raise Exception('token解析失败')
            elif int(time.time()) >= jwt_decode.get('exp'):  # 解析token成功时间超时
                raise Exception('token超时')
            else:
                logger.error(f'openid:[{jwt_decode.get("data").get("open_id")}] 访问:[{request.url_rule}]')
        else:
            raise Exception('登陆token为空，请重新登陆')

    except Exception as e:
        logger.error(f'异常: {e}')
        logger.error(f'重新授权登陆')
        # 当token不存在的时候重定向到授权页面
        # 当token超时时重新授权登陆
        res = redirect(login())
        res.headers['Content-Type'] = 'url'
        return res
