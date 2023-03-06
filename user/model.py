from datetime import datetime

from start import db


# 计数表
class Users(db.Model):
    # 设置结构体表格名称
    __tablename__ = 'Users'

    # 设定结构体对应表格的字段
    id = db.Column(db.Integer, primary_key=True)
    openid = db.Column(db.String, nullable=False)  # 用户唯一标识
    nickname = db.Column(db.String, nullable=False)  # 用户名称
    sex = db.Column(db.String, nullable=True)  # 用户性别
    province = db.Column(db.String, nullable=True)  # 省份
    city = db.Column(db.String, nullable=True)  # 城市
    country = db.Column(db.String, nullable=True)  # 国家
    headimgurl = db.Column(db.String, nullable=True)  # 用户头像
    privilege = db.Column(db.String, nullable=True)  # 用户特权信息
    unionid = db.Column(db.String, nullable=True)  # 只有在用户将公众号绑定到微信开放平台后才会出现
    level = db.Column(db.Integer, nullable=False)  # 用户类型




