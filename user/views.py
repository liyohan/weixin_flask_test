import logging
import requests
import config
import time

from flask import request, make_response, render_template
from user.model import Users
from start.response import make_succ_empty_response, make_succ_response, make_err_response
from sqlalchemy.exc import OperationalError

from user import user_app
from start import db
from start.views import login
from start.middlewares import token_encode

logger = logging.getLogger('log')


@user_app.route('/')
def get_user():

    openid = request.headers.get('x-wx-openid')
    source = request.headers.get('x-wx-source')

    data = {'headers': request.headers}
    return make_succ_response(f'测试{request.args}; data={data}')

'''
#             counter = Counters()
#             counter.id = 1
#             counter.count = 1
#             counter.created_at = datetime.now()
#             counter.updated_at = datetime.now()
#             insert_counter(counter)
#     counter = Counters.query.filter(Counters.id == 1).first()
#     return make_succ_response(0) if counter is None else make_succ_response(counter.count)

'''
def get_user_info(access_token, openid):
    """
    请求用户信息
    :param access_token:
    :param openid:
    :return:
    """
    url = f'https://api.weixin.qq.com/sns/userinfo?access_token={access_token}&openid={openid}&lang=zh_CN'
    res = requests.get(url).json()
    return res


@user_app.route('/get_access_token/')
def get_access_token():
    """
    获取授权用户信息
    """
    logger.error('获取授权用户信息')
    code = request.args.get('code')
    logger.error(code)

    # 获取用户access token
    url = f'https://api.weixin.qq.com/sns/oauth2/access_token?appid={config.app_id}&secret={config.app_secret}&code={code}&grant_type=authorization_code'
    res = requests.get(url).json()
    if res.get('access_token'):
        access_token, expires_in, open_id, refresh_token = res.get('access_token'), res.get('expires_in'), res.get(
            'openid'), res.get('refresh_token')

        user_data = Users.query.filter(Users.openid == open_id).first()
        # user_data = operation_db(f'select * from user where open_id="{open_id}"')
        logger.error(user_data)
        if user_data:
            logger.error(f'用户: {open_id} 已注册，将重新授权')
            # 若用户已经注册过，则只需要重新赋予token即可
            access_token_time = (int(time.time()) + expires_in) * 1000

            # operation_db(
            #     f'update user_token set access_token_time={access_token_time}, access_token="{access_token}" where open_id="{open_id}"')
            # logger.debug(f'用户: {open_id} 表数据已更新')

        else:
            logger.error(f'用户: {open_id} 首次注册')

            # 首次授权时才会写入数据库中
            # 请求微信服务器获取用户信息
            logger.error(f'获取用户信息 acces_token: {access_token} open_id: {open_id}')
            user_data = get_user_info(access_token, open_id)

            # 计算过期时间
            new_tiem = int(time.time())
            access_token_time = (new_tiem + expires_in) * 1000
            refresh_token_time = (new_tiem + 60 * 60 * 24 * 29) * 1000

            # 数据存储进数据库中
            users = Users()
            users.openid = open_id
            users.nickname = user_data.get('nickname')
            users.sex = user_data.get('sex')
            users.province = user_data.get('province')
            users.city = user_data.get('city')
            users.country = user_data.get('country')
            users.headimgurl = user_data.get('headimgurl')
            users.privilege = user_data.get('privilege')
            users.unionid = user_data.get('unionid')
            users.level = 0

            try:
                db.session.add(users)
                db.session.commit()
            except OperationalError as e:
                logger.error("insert_counter errorMsg= {} ".format(e))

            # db = get_db().cursor()
            # db.execute('replace INTO user_token (open_id,access_token,access_token_time,refresh_token,refresh_token_time) '
            #            'VALUES (?,?,?,?,?)', (open_id, access_token, access_token_time, refresh_token, refresh_token_time))
            # db.execute('replace INTO user (open_id,nickname,sex,province,city,country,headimgurl,privilege,unionid,level) '
            #            'VALUES (?,?,?,?,?,?,?,?,?,?)', (
            #                open_id, user_data.get('nickname'), user_data.get('sex'), user_data.get('province'),
            #                user_data.get('city'), user_data.get('country'), user_data.get('headimgurl'),
            #                str(user_data.get('privilege')),
            #                user_data.get('unionid'), 0))
            #
            # get_db().commit()
            # db.close()

        # 返回用户信息网页
        res = make_response(render_template('star/templates/home.html', open_url=login()))
        res.headers['Content-Type'] = 'html'

        # token获取
        token = token_encode(open_id, access_token, expires_in)
        res.headers['token'] = token
        return res

    # 当访问异常时
    else:
        logger.error(f'code用户[{code}]授权错误')
        pass
