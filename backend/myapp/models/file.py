# -*- coding: utf-8 -*-

from flask import current_app

from myapp.libs.mc import rdb
from myapp.libs.ext import db
from myapp.models.base import BaseMixin
from myapp.libs.file_cos import delete_cos, FILE_SITE


class Files(BaseMixin, db.Model):
    __tablename__ = 'files'

    STATUSES = (
        STATUS_UNPUBLISHED,
        STATUS_ONLINE
    ) = range(2)

    filename = db.Column(db.String(128), default='')
    file_md = db.Column(db.String(128), default='')
    pic_md = db.Column(db.String(128), default='')
    author = db.Column(db.String(128), default='')
    size = db.Column(db.String(64), default='')
    intro = db.Column(db.Text, default='')
    status = db.Column(db.Integer, default=STATUS_UNPUBLISHED)

    @classmethod
    def get_files(cls, page=1):
        query = Files.query.order_by(Files.created_at.desc())
        files = query.paginate(page, current_app.config['FILE_PAGE'])
        return files

    @property
    def file_url(self):
        return f'{FILE_SITE}{self.file_md}'

    @property
    def pic_url(self):
        return f'{FILE_SITE}{self.pic_md}'

    def delete(self):
        delete_cos(self.file_md)
        delete_cos(self.pic_md)
        super().delete()

    @classmethod
    def __flush_event__(cls, target):
        try:
            rdb.delete(*rdb.keys('files:*'))
        except:
            pass
