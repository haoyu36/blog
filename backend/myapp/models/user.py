# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

import jwt
from flask import current_app
from werkzeug.security import check_password_hash, generate_password_hash

from myapp.libs.ext import db
from myapp.models.base import BaseMixin


class AdminUser(BaseMixin, db.Model):
    __tablename__ = 'adminusers'
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    @classmethod
    def create(cls, **kwargs):
        password = kwargs.pop('password')
        kwargs['password'] = generate_password_hash(password)
        return super().create(**kwargs)

    def check_password(self, password):
        '''验证密码是否匹配'''
        return check_password_hash(self.password, password)

    def get_jwt(self, expires_in=10800):
        '''用户登录后，发放有效的 JWT 并设置过期时间'''
        now = datetime.utcnow()
        payload = {
            'user_id': self.id,
            'user_name': self.username,
            'exp': now + timedelta(seconds=expires_in),    # 过期时间
            'iat': now,    # 签发时间
        }
        return jwt.encode(
            payload,
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_jwt(token):
        '''验证 JWT 的有效性'''
        try:
            payload = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256'])
        except:
            # Token过期，被修改，则验证失败
            return None
        return AdminUser.query.get(payload.get('user_id'))
