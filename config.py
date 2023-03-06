import os

# 是否开启debug模式
DEBUG = True

# 读取数据库环境变量
username = os.environ.get("MYSQL_USERNAME", 'root')
# password = os.environ.get("MYSQL_PASSWORD", 'root')
password = os.environ.get("MYSQL_PASSWORD", 'GUB_RTADGF')
db_address = os.environ.get("MYSQL_ADDRESS", '127.0.0.1:3306')


# 公众号参数
app_id = os.environ.get('APPID', 'wx99bbd6f75d0588e6')
scope = os.environ.get('SCOPE', 'snsapi_userinfo')
