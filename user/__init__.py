from flask import Blueprint

# 加载蓝图
user_app = Blueprint('user', __name__, url_prefix='/user')



