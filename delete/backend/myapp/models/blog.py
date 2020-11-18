import os
from datetime import datetime, timedelta

import jwt
from flask import abort, current_app
from werkzeug.security import generate_password_hash, check_password_hash

from .base import BaseMixin
from .mc import rdb, cache
from .utils import is_numeric, NotAllowedException
from ..ext import db


MC_KEY_ALL_TAGS = 'tags:all_tags'
MC_KEY_TAGS_BY_POST = 'tags:post:%s:tags'
MC_KEY_POST_STATS_BY_TAG = 'tags:count_by_tags:%s'

MC_KEY_POSTS = 'posts:posts:%s'
MC_KEY_POSTS_BY_TAG = 'posts:posts_by_tags:%s:%s'


PER_PAGE = int(os.getenv('PER_PAGE'))


class Post(BaseMixin, db.Model):
    __tablename__ = 'posts'
    title = db.Column(db.String(128), default='')
    intro = db.Column(db.Text, default='')
    body = db.Column(db.Text, default='')
    html_body = db.Column(db.Text, default='')

    __table_args__ = (
        db.Index('idx_title', title),
    )

    @property
    @cache(MC_KEY_TAGS_BY_POST % ('{self.id}'))
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
    @cache(MC_KEY_POSTS % ('{page}'))
    def get_posts(cls, page=1):
        query = Post.query.order_by(Post.created_at.desc())
        posts = query.paginate(page, PER_PAGE)
        del posts.query     # Fix `TypeError: can't pickle _thread.lock objects`
        return posts

    @classmethod
    def get(cls, identifier):
        if is_numeric(identifier):
            return cls.cache.get(identifier)
        return cls.cache.filter(title=identifier).first()

    @classmethod
    def get_or_404(cls, ident):
        if not is_numeric(ident):
            abort(404)
        rv = cls.get(ident)
        if rv is None:
            rdb.delete('posts.id[{}]'.format(ident))
            abort(404)
        return rv

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

    @classmethod
    def __flush_event__(cls, target):
        try:
            rdb.delete(*rdb.keys('posts:*'))
        except:
            pass


class Tag(BaseMixin, db.Model):
    __tablename__ = 'tags'
    name = db.Column(db.String(128), default='', unique=True)

    __table_args__ = (
        db.Index('idx_name', name),
    )

    @classmethod
    @cache(MC_KEY_ALL_TAGS)
    def get_all_tag(cls):
        tags_lst = [t.name for t in Tag.query.all()]
        return tags_lst

    @classmethod
    def get_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

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
            rdb.delete(*rdb.keys('tags:*'))
        except:
            pass


class PostTag(BaseMixin, db.Model):
    __tablename__ = 'post_tags'
    post_id = db.Column(db.Integer)
    tag_id = db.Column(db.Integer)

    __table_args__ = (
        db.Index('idx_post_id', post_id),
        db.Index('idx_tag_id', tag_id),
    )

    @classmethod
    def _get_posts_by_tag(cls, identifier):
        if not identifier:
            return []
        if not is_numeric(identifier):
            tag = Tag.get_by_name(identifier)
            if not tag:
                return
            identifier = tag.id
        at_ids = cls.query.with_entities(cls.post_id).filter(
            cls.tag_id == identifier
        ).all()

        query = Post.query.filter(
            Post.id.in_(id for id, in at_ids)).order_by(Post.id.desc())
        return query

    @classmethod
    @cache(MC_KEY_POSTS_BY_TAG % ('{identifier}', '{page}'))
    def get_posts_by_tag(cls, identifier, page=1):
        query = cls._get_posts_by_tag(identifier)
        posts = query.paginate(page, PER_PAGE)
        del posts.query  # Fix `TypeError: can't pickle _thread.lock objects`
        return posts

    @classmethod
    @cache(MC_KEY_POST_STATS_BY_TAG % ('{identifier}'))
    def get_count_by_tag(cls, identifier):
        query = cls._get_posts_by_tag(identifier)
        return query.count()

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
            PostTag.query.filter_by(post_id=post_id, tag_id=tag_id).first().delete()
        for tag_id in need_add_tag_ids:
            cls.create(post_id=post_id, tag_id=tag_id)
        db.session.commit()

    @classmethod
    def __flush_event__(cls, target):
        try:
            rdb.delete(*rdb.keys('tags:*'))
        except:
            pass
        try:
            rdb.delete(*rdb.keys('posts:posts_by_tags:*'))
        except:
            pass


class AdminUser(BaseMixin, db.Model):
    __tablename__ = 'adminusers'
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    @classmethod
    def create_user(cls, username, password):
        password_hash = generate_password_hash(password)
        ok, user = AdminUser.create(username=username, password_hash=password_hash)
        return user

    def check_password(self, password):
        # 验证密码是否匹配
        return check_password_hash(self.password_hash, password)

    def get_jwt(self, expires_in=1200):
        '''用户登录后，发放有效的 JWT，过期时间20分钟'''
        now = datetime.utcnow()
        payload = {
            'user_id': self.id,
            'user_name': self.username,
            'exp': now + timedelta(seconds=expires_in),    # 过期时间
            'iat': now          # 签发时间
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
        except (jwt.exceptions.ExpiredSignatureError,
                jwt.exceptions.InvalidSignatureError,
                jwt.exceptions.DecodeError) as e:
            # Token过期，或被修改，则验证失败
            return None
        return AdminUser.query.get(payload.get('user_id'))


class Files(BaseMixin, db.Model):
    __tablename__ = 'files'
    name = db.Column(db.String(128), default='')
    size = db.Column(db.String(64))

    __table_args__ = (
        db.Index('idx_name', name),
    )

    @classmethod
    def __flush_event__(cls, target):
        try:
            rdb.delete(*rdb.keys('files:*'))
        except:
            pass
