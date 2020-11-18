#!/usr/bin/env python
# -*- coding: utf-8 -*-


from datetime import datetime
from ..ext import db


class BaseMixin:
    @classmethod
    def get_db_props(cls, kwargs):
        props = {}
        for col, default in cls._db_columns:
            props[col] = kwargs.pop(col, default)
        return props

    @classmethod
    def create_or_update(cls, **kwargs):
        session = db.session
        props = cls.get_db_props(kwargs)
        id = kwargs.pop('id', None)
        if id is not None:
            obj = cls.query.get(id)
            if obj:
                if 'updated_at' not in kwargs:
                    kwargs['updated_at'] = datetime.now()
                for k, v in kwargs.items():
                    setattr(obj, k, v)
                session.commit()
                cls.update_db_props(obj, props)
                return False, obj
        obj = cls(**kwargs)
        obj.save()
        cls.update_db_props(obj, props)
        return True, obj

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.save()

    @classmethod
    def create(cls, **kwargs):
        props = cls.get_db_props(kwargs)
        if not kwargs:
            return False, None
        filter = cls.query.filter_by(**kwargs)
        obj = filter.first()
        if obj:
            return False, obj
        obj = cls(**kwargs)
        obj.save()
        cls.update_db_props(obj, props)
        return True, obj

    @classmethod
    def update_db_props(cls, obj, db_props):
        for prop, value in db_props.items():
            obj.set_props_item(prop, value)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
