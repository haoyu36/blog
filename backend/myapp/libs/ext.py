# -*- coding: utf-8 -*-
'''
统一管理 Flask 扩展 
'''

from datetime import datetime
from flask import abort

from sqlalchemy import Column, DateTime, Integer, event
from flask_sqlalchemy import SQLAlchemy, Model


class BaseModel(Model):

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=None)

    __table_args__ = {'mysql_charset': 'utf8mb4', 'extend_existing': True}

    def __repr__(self):
        return '<{0} id: {1}>'.format(self.__class__.__name__, self.id)

    @classmethod
    def get(cls, id):
        return cls.query.get(id)

    @classmethod
    def get_or_404(cls, ident):
        rv = cls.get(ident)
        if rv is None:
            abort(404)
        return rv

    @classmethod
    def get_multi(cls, ids):
        return [cls.get(id) for id in ids]

    @property
    def path(self):
        return '/{}/{}/'.format(self.__class__.__name__.lower(), self.id)

    def to_dict(self):
        columns = self.__table__.columns.keys()
        dct = {key: getattr(self, key, None) for key in columns}
        return dct

    @staticmethod
    def _flush_insert_event(mapper, connection, target):
        target._flush_event(mapper, connection, target)
        target.__flush_insert_event__(target)

    @staticmethod
    def _flush_after_update_event(mapper, connection, target):
        target._flush_event(mapper, connection, target)
        target.__flush_after_update_event__(target)

    @staticmethod
    def _flush_delete_event(mapper, connection, target):
        target._flush_event(mapper, connection, target)
        target.__flush_delete_event__(target)

    # mapper: 映射器，映射为目标数据库
    # 连接对象: 为此实例的目标数据库提供了当前事务的句柄
    # 目标对象: 即当前操作数据库的实例对象
    @staticmethod
    def _flush_event(mapper, connection, target):
        target.__flush_event__(target)

    @classmethod
    def __flush_event__(cls, target):
        pass

    @classmethod
    def __flush_delete_event__(cls, target):
        pass

    @classmethod
    def __flush_insert_event__(cls, target):
        pass

    @classmethod
    def __flush_after_update_event__(cls, target):
        pass

    @classmethod
    def __declare_last__(cls):
        '''
        调用 sqlalchemy 提供的一些事件，用于清除缓存。分别对应于
        在发出与该实例对应的 DELETE 语句后接收对象实例;
        在发出与该实例对应的INSERT语句后接收对象实例;
        在发出对应于该实例的UPDATE语句之后接收对象实例;
        '''
        event.listen(cls, 'after_delete', cls._flush_delete_event)
        event.listen(cls, 'after_update', cls._flush_after_update_event)
        event.listen(cls, 'after_insert', cls._flush_insert_event)


db = SQLAlchemy(model_class=BaseModel)
