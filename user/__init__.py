from flask import Blueprint


# 加载蓝图
from run import app

user_app = Blueprint('user', __name__, url_prefix='/user')
app.register_blueprint(user_app)



