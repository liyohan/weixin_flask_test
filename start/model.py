from datetime import datetime

from start import db


# 计数表
class Counters(db.Model):
    # 设置结构体表格名称
    __tablename__ = 'Counters'

    # 设定结构体对应表格的字段
    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer, default=1)
    created_at = db.Column('createdAt', db.TIMESTAMP, nullable=False, default=datetime.now())
    updated_at = db.Column('updatedAt', db.TIMESTAMP, nullable=False, default=datetime.now())


# 商品表
class Works(db.Model):
    # 设置结构体表格名称
    __tablename__ = 'Works'

    # 设定结构体对应表格的字段
    id = db.Column(db.Integer, primary_key=True)
    pay = db.Column(db.Integer, nullable=False)
    settle = db.Column(db.Text, nullable=False)
    place = db.Column(db.Text, nullable=False)
    phone = db.Column(db.Integer, nullable=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    describe = db.Column(db.Text, nullable=True)
    pid = db.Column(db.Integer, nullable=False)
    frist_time = db.Column(db.DateTime, nullable=False, default=datetime.now())
    update_time = db.Column(db.DateTime, nullable=False, default=datetime.now())
    hide = db.Column(db.Integer, nullable=False, default=0)