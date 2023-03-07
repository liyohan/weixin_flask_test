from flask import Blueprint

# 加载蓝图
work_app = Blueprint('work', __name__, url_prefix='/work')