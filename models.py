from datetime import datetime

from flask_login import UserMixin
from ext import db, app, login_manager
from werkzeug.security import generate_password_hash, check_password_hash


class BaseModel:
    def create(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def save(self):
        db.session.commit()



movie_genres = db.Table(
    'movie_genres',
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('genres.id'), primary_key=True)
)


class Movie(db.Model, BaseModel):
    __tablename__ = "movie"

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.ForeignKey("category.id"))
    title = db.Column(db.String)
    desc = db.Column(db.String)
    imbd = db.Column(db.Float)
    imgv = db.Column(db.String)
    imgh = db.Column(db.String)
    category = db.relationship("Category")
    genres = db.relationship('Genre', secondary=movie_genres, backref=db.backref('movies', lazy='dynamic'))
    comments_relation = db.relationship('Comment', backref=db.backref('movie_rel'))

class Genre(db.Model):

    __tablename__ = "genres"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)

class Category(db.Model, BaseModel):

    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String)

    filmss = db.relationship("Movie")

class User(db.Model, BaseModel, UserMixin):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    role = db.Column(db.String)

    def __init__(self, username, password, role="user"):
        self.username = username
        self.password = generate_password_hash(password)
        self.role = role


    def check_password(self, password):
        return check_password_hash(self.password, password)

class Comment(db.Model, BaseModel):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())

    movie = db.relationship('Movie', backref=db.backref('comments_rel'))
    user = db.relationship('User', backref=db.backref('comments', lazy='dynamic'))



@db.event.listens_for(Comment, 'before_insert')
def add_timestamp(mapper, connection, target):
    target.timestamp = datetime.utcnow()



@login_manager.user_loader
def load_user(user_id):
    return  User.query.get(user_id)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()







#        new_user = User(username ="admin", password="hondagrom125", role="admin")
#        new_category = Category(id=1,category="ფილმები")
#        new_category = Category(id=2,category="სერიალები")
#        new_movie = Movie(category_id=1, title="title222", desc="desc222", imbd=3.3, imgv="ara222", imgh="ara222", genre="rara222")
#        new_category.create()


