# 创建应用实例
import sys

from start import app

from user import user_app
from buys import work_app

app.register_blueprint(user_app)
app.register_blueprint(work_app)

# 启动Flask Web服务
if __name__ == '__main__':
    app.run(host=sys.argv[1], port=sys.argv[2])