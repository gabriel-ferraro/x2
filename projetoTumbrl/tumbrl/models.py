from tumbrl import database
from datetime import datetime
from tumbrl import login_manager
from flask_login import UserMixin
import uuid
from sqlalchemy.dialects.postgresql import UUID


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(database.Model, UserMixin):
    __tablename__ = 'user'
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False, unique=True)
    email = database.Column(database.String, nullable=False, unique=True)
    password = database.Column(database.String, nullable=False)
    posts = database.Relationship("Posts", backref='user', lazy=True)


class Posts(database.Model):
    __tablename__ = 'posts'
    id = database.Column(database.Integer, primary_key=True)
    post_text = database.Column(database.String, default='')
    post_img = database.Column(database.String, default='default.png')
    creation_date = database.Column(database.DateTime, nullable=False, default=datetime.utcnow())
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False)
    likes = database.Column(database.Integer, default=0)
    reposted_by = database.relationship('User', secondary='reposts', backref=database.backref('reposts', lazy='dynamic'))
    comments = database.relationship('User', secondary='comments', backref=database.backref('comments', lazy='dynamic'))


class Reposts(database.Model):
    __tablename__ = 'reposts'
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'), primary_key=True)
    post_id = database.Column(database.Integer, database.ForeignKey('posts.id'), primary_key=True)
    reposted_at = database.Column(database.DateTime, default=datetime.utcnow())


class Like(database.Model):
    __tablename__ = 'like'
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'), primary_key=True)
    post_id = database.Column(database.Integer, database.ForeignKey('posts.id'), primary_key=True)


class Comment(database.Model):
    __tablename__ = 'comments'
    text = database.Column(database.String, nullable=False)
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'), primary_key=True)
    post_id = database.Column(database.Integer, database.ForeignKey('posts.id'), primary_key=True)
    creation_date = database.Column(database.DateTime, nullable=False, default=datetime.utcnow())
