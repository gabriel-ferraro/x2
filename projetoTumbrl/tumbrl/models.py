# Aqui vai a estrutura do nosso banco de dados (classes e tals)
from tumbrl import database
from datetime import datetime
from tumbrl import login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(database.Model, UserMixin):
    __table_args__ = {'extend_existing': True}
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False, unique=True)
    email = database.Column(database.String, nullable=False, unique=True)
    password = database.Column(database.String, nullable=False)
    posts = database.Relationship("Posts", backref='user', lazy=True)


class Posts(database.Model):
    __tablename__ = 'posts'
    __table_args__ = {'extend_existing': True}
    id = database.Column(database.Integer, primary_key=True)
    post_text = database.Column(database.String, default='')
    post_img = database.Column(database.String, default='default.png')
    creation_date = database.Column(database.DateTime, nullable=False, default=datetime.utcnow())
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False)
    likes = database.Column(database.Integer, default=0)


class Like(database.Model):
    __tablename__ = 'likes'
    __table_args__ = {'extend_existing': True}
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'), primary_key=True)
    post_id = database.Column(database.Integer, database.ForeignKey('posts.id'), primary_key=True)
