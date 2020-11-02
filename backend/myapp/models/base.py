# -*- coding: utf-8 -*-

from datetime import datetime
from myapp.libs.ext import db


class BaseMixin:

    @classmethod
    def create_or_update(cls, **kwargs):
        session = db.session
        id = kwargs.pop('id', None)
        if id is not None:
            obj = cls.query.get(id)
            if obj:
                if 'updated_at' not in kwargs:
                    kwargs['updated_at'] = datetime.now()
                for k, v in kwargs.items():
                    setattr(obj, k, v)
                session.commit()
                return False, obj
        obj = cls(**kwargs)
        obj.save()
        return True, obj

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.save()

    @classmethod
    def create(cls, **kwargs):
        if not kwargs:
            return False, None
        filter = cls.query.filter_by(**kwargs)
        obj = filter.first()
        if obj:
            return False, obj
        obj = cls(**kwargs)
        obj.save()
        return True, obj

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
