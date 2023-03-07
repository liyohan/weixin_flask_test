from flask import request
from flask import Blueprint

# 加载蓝图
work_app = Blueprint('work', __name__, url_prefix='/work')

from buys.model import Works
from start import db

import time
from sqlalchemy.exc import OperationalError
from start.response import *


import logging
logger = logging.getLogger('log')


@work_app.route('/get_data/')
def get_works_data():
    """
    获取工作信息
    :return: {'code':状态, 'msg':说明, 'data':写入状态}
    """
    # 若get请求中带有openid，则获取该openid下所有发布信息
    # openid = request.args.get('open_id')
    # sql = 'select * from works'
    # if openid:
    #     id_sql = f'select id from user where open_id="{openid}"'  # hide=0'
    #     id = operation_db(id_sql)[0].get('id')
    #     sql += f' where pid={id}'
    #
    # return operation_db(sql)
    work = Works.query.filter().first()
    return make_succ_response(work)



@work_app.route('/save_data/', methods=['POST'])
def save_works_data():
    """
    添加工作信息
    :return: {'code':状态, 'msg':说明, 'data':写入状态}
    """
    try:
        data = request.json()
        work = Works()
        work.pay = data.get('pay')
        work.settle = data.get('settle')
        work.place = data.get('place')
        work.phone = data.get('phone')
        work.title = data.get('title')
        work.content = data.get('content')
        work.describe = data.get('describe')
        work.pid = data.get('pid')

        try:
            db.session.add(work)
            db.session.commit()
        except OperationalError as e:
            logger.error("insert_counter errorMsg= {} ".format(e))



        return {'code': 0, 'msg': '', 'data': True}
    except Exception as e:
        return {'code': 1, 'msg': '写入异常', 'data': ""}


# @work_app.route('/remove_data/', methods=['POST'])
# def remove_works_data():
#     """
#     删除工作信息
#     :return: {'code':状态, 'msg':说明, 'data':写入状态}
#     """
#     try:
#         data = request.json
#         id = data.get('id')
#         openid = token_decode(request.headers.get('token')).get('data').get('open_id')
#
#         # 判断是否符合
#         pid = operation_db(f'select pid from works where id={id}')[0].get('pid')
#         openid_user = operation_db(f'select open_id from user where id={pid}')[0].get('open_id')
#
#         # 判断是否为创建人，若不是则返回异常
#         if openid_user != openid:
#             raise Exception("创建人异常请确认！！")
#
#         # 删除记录(隐形删除)
#         operation_db(f'update works set hide=1, update_time={time.time()} where id={id}')
#         return {'code': 0, 'msg': '', 'data': True}
#
#     except Exception as e:
#         return {'code': 1, 'msg': "删除异常", 'data': str(e)}
#
#
# @work_app.route('/update_data/', methods=['POST'])
# def update_works_data():
#     """
#     更新工作信息
#     :return: {'code':状态, 'msg':说明, 'data':写入状态}
#     """
#     try:
#         data = request.json
#         id = data.get('id')
#         openid = token_decode(request.headers.get('token')).get('data').get('open_id')
#         body = {
#             'pay': data.get('pay'),
#             'settle': data.get('settle'),
#             'place': data.get('place'),
#             'phone': data.get('phone'),
#             'title': data.get('title'),
#             'content': data.get('content'),
#             'describe': data.get('describe')
#         }
#
#         # 判断是否符合
#         pid = operation_db(f'select pid from works where id={id}')[0].get('pid')
#         openid_user = operation_db(f'select open_id from user where id={pid}')[0].get('open_id')
#
#         # 判断是否为创建人，若不是则返回异常
#         if openid_user != openid:
#             raise Exception("创建人异常请确认！！")
#
#         # 拼接传递参数
#         sql_update = []
#         for key, value in body.items():
#             if value:
#                 sql_update.append(f'{key}="{value}"')
#
#         # 更新数据
#         operation_db(f'update works set {",".join(sql_update)} where id={id}')
#         return {'code': 0, 'msg': '', 'data': True}
#
#     except Exception as e:
#         return {'code': 1, 'msg': "更新异常", 'data': str(e)}
