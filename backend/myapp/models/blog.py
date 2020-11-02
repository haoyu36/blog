# -*- coding: utf-8 -*-

from flask import current_app

from myapp.libs.ext import db
from myapp.libs.mc import rdb
from myapp.libs.utils import NotAllowedException
from myapp.libs.md import markdown, toc, toc_md
from myapp.models.base import BaseMixin


class Post(BaseMixin, db.Model):
    __tablename__ = 'posts'

    # 状态管理仅用于后台示例，博客均与状态无关
    STATUSES = (
        STATUS_UNPUBLISHED,
        STATUS_ONLINE
    ) = range(2)

    title = db.Column(db.String(128), default='')
    intro = db.Column(db.Text, default='')
    body = db.Column(db.Text, default='')
    status = db.Column(db.Integer, default=STATUS_UNPUBLISHED)

    @property
    def tags(self):
        at_ids = PostTag.query.with_entities(
            PostTag.tag_id).filter(
                PostTag.post_id == self.id
        ).all()

        tags = Tag.query.filter(Tag.id.in_((id for id, in at_ids))).all()
        return tags

    def update_tags(self, tagnames):
        PostTag.update_multi(self.id, tagnames)
        return True

    @classmethod
    def get_posts(cls, page=1):
        query = Post.query.order_by(Post.created_at.desc())
        posts = query.paginate(page, current_app.config['PER_PAGE'])
        return posts

    @classmethod
    def create_or_update(cls, **kwargs):
        tags = kwargs.pop('tags', [])
        created, obj = super(Post, cls).create_or_update(**kwargs)
        if tags:
            PostTag.update_multi(obj.id, tags, [])
        return created, obj

    def delete(self):
        id = self.id
        super().delete()
        for pt in PostTag.query.filter_by(post_id=id):
            pt.delete()

    @property
    def html(self):
        body = self.body
        if not body:
            return ''
        return markdown(body)

    @property
    def toc(self):
        body = self.body
        if not body:
            return ''
        toc.reset_toc()
        toc_md.parse(body)
        return toc.render_toc(level=3)

    @classmethod
    def __flush_event__(cls, target):
        try:
            rdb.delete(*rdb.keys('api:*'))
        except:
            pass


class Tag(BaseMixin, db.Model):
    __tablename__ = 'tags'

    name = db.Column(db.String(128), default='', unique=True)

    @classmethod
    def create(cls, **kwargs):
        name = kwargs.pop('name')
        kwargs['name'] = name.lower()
        return super().create(**kwargs)

    def delete(self):
        raise NotAllowedException

    def update(self, **kwargs):
        raise NotAllowedException

    @classmethod
    def __flush_event__(cls, target):
        try:
            rdb.delete(*rdb.keys('api:tags'))
        except:
            pass


class PostTag(BaseMixin, db.Model):
    __tablename__ = 'post_tags'

    post_id = db.Column(db.Integer)
    tag_id = db.Column(db.Integer)

    @classmethod
    def _get_posts_by_tag(cls, identifier):
        if not identifier:
            return []
        at_ids = cls.query.with_entities(cls.post_id).filter(
            cls.tag_id == identifier
        ).all()

        query = Post.query.filter(
            Post.id.in_(id for id, in at_ids)).order_by(Post.id.desc())
        return query

    @classmethod
    def get_count_by_tag(cls, identifier):
        query = cls._get_posts_by_tag(identifier)
        return query.count()

    @classmethod
    def get_posts_by_tag(cls, identifier, page=1):
        query = cls._get_posts_by_tag(identifier)
        posts = query.paginate(page, current_app.config['PER_PAGE'])
        return posts

    @classmethod
    def update_multi(cls, post_id, tags, origin_tags=None):
        if origin_tags is None:
            origin_tags = [t.name for t in Post.get(post_id).tags]
        need_add = set()
        need_del = set()
        for tag in tags:
            if tag not in origin_tags:
                need_add.add(tag)
        for tag in origin_tags:
            if tag not in tags:
                need_del.add(tag)
        need_add_tag_ids = set()
        need_del_tag_ids = set()
        for tag_name in need_add:
            _, tag = Tag.create(name=tag_name)
            need_add_tag_ids.add(tag.id)
        for tag_name in need_del:
            _, tag = Tag.create(name=tag_name)
            need_del_tag_ids.add(tag.id)

        for tag_id in need_del_tag_ids:
            PostTag.query.filter_by(
                post_id=post_id, tag_id=tag_id).first().delete()
        for tag_id in need_add_tag_ids:
            cls.create(post_id=post_id, tag_id=tag_id)
        db.session.commit()

    @classmethod
    def __flush_event__(cls, target):
        try:
            rdb.delete(*rdb.keys('api:*'))
        except:
            pass
