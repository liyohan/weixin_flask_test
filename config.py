import os

# 是否开启debug模式
DEBUG = True

# 读取数据库环境变量
username = os.environ.get("MYSQL_USERNAME", 'root')
password = os.environ.get("MYSQL_PASSWORD", 'root')
# password = os.environ.get("MYSQL_PASSWORD", 'GUB_RTADGF')
db_address = os.environ.get("MYSQL_ADDRESS", '127.0.0.1:3306')


# 公众号参数
app_id = os.environ.get('APPID', 'wx99bbd6f75d0588e6')
app_secret = os.environ.get('APPSECRET', '24685d0c60fd649f590105b0aad3341c')
scope = os.environ.get('SCOPE', 'snsapi_userinfo')
token_user = os.environ.get('TOKEN_USER', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9')
issuer = os.environ.get('ISSUER', 'Ming_lyon')
