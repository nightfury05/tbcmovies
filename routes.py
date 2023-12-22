from flask import render_template, redirect, flash, url_for
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy.orm import joinedload
from sqlalchemy import desc
from os import path

from forms import AddMovieForm, RegisterForm, EditMovieForm, LoginForm, CommentForm
from models import Movie, Genre, movie_genres, Category, User, Comment
from ext import app, db

library = "Flask 2,0"
#films = [
  #  {"title": "Mission imposable", "desc": "movie description", "imgv": "Mission_imposable_v.jpg",
  #   "imgh": "Mission_Impossible_7_h.jpg", "imbd": "6.9"},
  #  {"title": "Grand Turismo", "desc": "movie description2", "imgv": "grand_turismo_v.jpg",
  #   "imgh": "Grand_turismo_h.jpg", "imbd": "6.9"},
  #  {"title": "Blue Beetle", "desc": "movie description3", "imgv": "blue_beetle_v.jpg", "imgh": "Blue_Beetle_j.jpg",
  #   "imbd": "6.9"},
  #  {"title": "Blue Beetle", "desc": "movie description3", "imgv": "blue_beetle_v.jpg", "imgh": "Blue_Beetle_j.jpg",
  #   "imbd": "6.9"},
  #  {"title": "Blue Beetle", "desc": "movie description3", "imgv": "blue_beetle_v.jpg", "imgh": "Blue_Beetle_j.jpg",
  #   "imbd": "6.9"},
  #  {"title": "Blue Beetle", "desc": "movie description3", "imgv": "blue_beetle_v.jpg", "imgh": "Blue_Beetle_j.jpg",
  #   "imbd": "6.9"},
  #  {"title": "Blue Beetle", "desc": "movie description3", "imgv": "blue_beetle_v.jpg", "imgh": "Blue_Beetle_j.jpg",
  #   "imbd": "6.9"},
  #  {"title": "Mission imposable", "desc": "movie description", "imgv": "Mission_imposable_v.jpg",
  #   "imgh": "Mission_Impossible_7_h.jpg", "imbd": "6.9"},
  #  {"title": "Blue Beetle", "desc": "movie description3", "imgv": "blue_beetle_v.jpg", "imgh": "Blue_Beetle_j.jpg",
   #   "imbd": "6.9"},
  #  {"title": "Grand Turismo", "desc": "movie description2", "imgv": "grand_turismo_v.jpg",
  #   "imgh": "Grand_turismo_h.jpg", "imbd": "6.9"},
  #  {"title": "Mission imposable", "desc": "movie description", "imgv": "Mission_imposable_v.jpg",
  #   "imgh": "Mission_Impossible_7_h.jpg", "imbd": "6.9"},
  #  {"title": "Grand Turismo", "desc": "movie description2", "imgv": "grand_turismo_v.jpg",
  #   "imgh": "Grand_turismo_h.jpg", "imbd": "6.9"},
  #  {"title": "Blue Beetle", "desc": "movie description3", "imgv": "blue_beetle_v.jpg", "imgh": "Blue_Beetle_j.jpg",
  #   "imbd": "6.9"},
  #  {"title": "Grand Turismo", "desc": "movie description2", "imgv": "grand_turismo_v.jpg",
  #   "imgh": "Grand_turismo_h.jpg", "imbd": "6.9"},
  #  {"title": "Blue Beetle", "desc": "movie description3", "imgv": "blue_beetle_v.jpg", "imgh": "Blue_Beetle_j.jpg",
  #   "imbd": "6.9"},
  #  {"title": "Grand Turismo", "desc": "movie description2", "imgv": "grand_turismo_v.jpg",
  #   "imgh": "Grand_turismo_h.jpg", "imbd": "6.9"},
  #  {"title": "Blue Beetle", "desc": "movie description3", "imgv": "blue_beetle_v.jpg", "imgh": "Blue_Beetle_j.jpg",
  #  "imbd": "6.9"},
  #  {"title": "Grand Turismo", "desc": "movie description2", "imgv": "grand_turismo_v.jpg",
  #   "imgh": "Grand_turismo_h.jpg", "imbd": "6.9"},
  #  {"title": "Blue Beetle", "desc": "movie description3", "imgv": "blue_beetle_v.jpg", "imgh": "Blue_Beetle_j.jpg",
  #   "imbd": "6.9"},
  #  {"title": "Grand Turismo", "desc": "movie description2", "imgv": "grand_turismo_v.jpg",
  #   "imgh": "Grand_turismo_h.jpg", "imbd": "6.9"},
 #   {"title": "Blue Beetle", "desc": "movie description3", "imgv": "blue_beetle_v.jpg", "imgh": "Blue_Beetle_j.jpg",
 #    "imbd": "6.9"},
   # {"title": "Grand Turismo", "desc": "movie description2", "imgv": "grand_turismo_v.jpg",
    # "imgh": "Grand_turismo_h.jpg", "imbd": "6.9"},
   # {"title": "Blue Beetle", "desc": "movie description3", "imgv": "blue_beetle_v.jpg", "imgh": "Blue_Beetle_j.jpg",
   #  "imbd": "6.9"},
  #  {"title": "Grand Turismo", "desc": "movie description2", "imgv": "grand_turismo_v.jpg",
 #    "imgh": "Grand_turismo_h.jpg", "imbd": "6.9"},]
#Series = [
  #  {"title": "LOKI", "desc": "serie description 111111111111111111", "imgv": "loki-v.jpeg", "imgh": "loki_h.jpg"},
#    {"title": "RICK AND MORTY", "desc": "serie description", "imgv": "rick_v.jpg", "imgh": "rick_h.jpg"},
 #   {"title": "AHSOKA ", "desc": "serie description", "imgv": "asoka_v.jpg", "imgh": "asoka_h.jpg"},
 #   {"title": "HEELS", "desc": "serie description", "imgv": "heels_v.jpg", "imgh": "heels_h.jpg"},
  #  {"title": "LOKI", "desc": "serie description", "imgv": "loki-v.jpeg", "imgh": "loki_h.jpg"},
   # {"title": "AHSOKA ", "desc": "serie description", "imgv": "asoka_v.jpg", "imgh": "asoka_h.jpg"},
  #  {"title": "HEELS", "desc": "serie description", "imgv": "heels_v.jpg", "imgh": "heels_h.jpg"},
  #  {"title": "LOKI", "desc": "serie description", "imgv": "loki-v.jpeg", "imgh": "loki_h.jpg"},
   # {"title": "LOKI", "desc": "serie description", "imgv": "loki-v.jpeg", "imgh": "loki_h.jpg"},
  #  {"title": "AHSOKA ", "desc": "serie description", "imgv": "asoka_v.jpg", "imgh": "asoka_h.jpg"},
  #  {"title": "HEELS", "desc": "serie description", "imgv": "heels_v.jpg", "imgh": "heels_h.jpg"},
  #  {"title": "LOKI", "desc": "serie description", "imgv": "loki-v.jpeg", "imgh": "loki_h.jpg"},
 #   {"title": "LOKI", "desc": "serie description", "imgv": "loki-v.jpeg", "imgh": "loki_h.jpg"},]
Series = []


@app.route("/")
def index():
    films = Movie.query.filter(Movie.category_id == 1).all()
    series = Movie.query.filter(Movie.category_id == 2).all()

    return render_template("main.html", films=films, series=series,)



@app.route("/category/<int:category_id>")
def mcategory(category_id):
    films = Movie.query.filter(Movie.category_id == category_id).all()
    return render_template("Movies.html", films=films)


@app.route("/Watch/<int:movie_id>", methods=['GET', 'POST'])
def Watch(movie_id):
    chosen_watch = Movie.query.options(joinedload(Movie.genres)).get(movie_id)
    user = User.username
    comments = Comment.query.filter(Comment.movie_id == movie_id).order_by(Comment.timestamp.desc()).all()
    form = CommentForm()
    if form.validate_on_submit():
        if chosen_watch:
            new_comment = Comment(text=form.text.data, user=current_user)
            chosen_watch.comments_relation.append(new_comment)
            db.session.add(new_comment)
            db.session.commit()
            return redirect(url_for('Watch', movie_id=movie_id,))

    if not chosen_watch:
        return render_template("404.html")
    genres = [genre.name for genre in chosen_watch.genres]
    return render_template("example.html", film=chosen_watch, genres=genres, form=form, user=user, comments=comments)


@app.route("/Add_Movie", methods=["GET", "POST"])
@login_required
def add_movie():
    form = AddMovieForm()
    selected_category_id = form.category_id.data
    category = Category.query.get(selected_category_id)

    if current_user.role != "admin":
        return redirect("/")

    if form.validate_on_submit():
        new_movie = Movie(
            title=form.title.data,
            desc=form.desc.data,
            imbd=form.imbd.data,
            imgv=form.imgv.data.filename,
            imgh=form.imgh.data.filename,
            category=category
        )

        genres = []
        for genre_name in form.genre.data:
            genre = Genre.query.filter_by(name=genre_name).first()
            if not genre:
                genre = Genre(name=genre_name)
            genres.append(genre)


        new_movie.genres.extend(genres)
        db.session.add(new_movie)
        db.session.commit()

        file_directoryv = path.join(app.root_path, "static", form.imgv.data.filename)
        file_directoryh = path.join(app.root_path, "static", form.imgh.data.filename)
        form.imgv.data.save(file_directoryv)
        form.imgh.data.save(file_directoryh)
        return redirect("/")
    else:
        print(form.errors)

    return render_template("add_movie.html", form=form)



@app.route("/edit_movie/<int:movie_id>", methods=["GET", "POST"])
@login_required
def edit_movie(movie_id):
    chosen_watch = Movie.query.get(movie_id)

    if not chosen_watch:
        return render_template("404.html")

    if current_user.role != "creator" and current_user.role != "admin":
        return redirect("/")

    form = EditMovieForm(title=chosen_watch.title, desc=chosen_watch.desc, imbd=chosen_watch.imbd, category_id=chosen_watch.category_id)
    genre_list = []
    for gname in chosen_watch.genres:
        genre_list.append(gname.name)

    form.genre.data = genre_list

    if form.validate_on_submit():
        chosen_watch.title = form.title.data
        chosen_watch.desc = form.desc.data
        chosen_watch.imbd = form.imbd.data
        chosen_watch.genres.clear()
        genres = []
        for genre_name in form.genre.data:
            genre = Genre.query.filter_by(name=genre_name).first()
            if not genre:
                genre = Genre(name=genre_name)
            genres.append(genre)

        chosen_watch.genres.extend(genres)

        if form.imgv.data:
            chosen_watch.imgv = form.imgv.data.filename
            file_directoryv = path.join(app.root_path, "static", form.imgv.data.filename)
            form.imgv.data.save(file_directoryv)
        if form.imgh.data:
            chosen_watch.imgh = form.imgh.data.filename
            file_directoryh = path.join(app.root_path, "static", form.imgh.data.filename)
            form.imgh.data.save(file_directoryh)

        chosen_watch.category_id = form.category_id.data

        db.session.commit()
        return redirect("/")

    return render_template("edit_movie.html", form=form)

@app.route("/delete_movie/<int:movie_id>")
@login_required
def delete_product(movie_id):
    chosen_watch = Movie.query.get(movie_id)
    if not chosen_watch:
        return render_template("404.html")

    if current_user.role != "admin":
        return redirect("/")
    chosen_watch.delete()
    return redirect("/")


@app.route("/search/<string:title>")
def search(title):
    films = Movie.query.filter(Movie.title.ilike(f"%{title}%")).all()
    return render_template("search.html", films=films)



@app.route('/genre/<genre_name>')
def movies_by_genre(genre_name):
    movie = Movie.query.join(movie_genres).join(Genre).filter(Genre.name == genre_name).all()

    return render_template('genre.html', genre=genre_name, films=movie)



@app.route("/Sign_Up", methods=["GET", "POST"])
def sign_up():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('მომხმარებელი უკვე არსებობს.')
        else:
            new_user = User(username=form.username.data, password=form.password.data, role="user")
            new_user.create()
            print(form.username.data)
            print(form.email.data)
            print(form.password.data)
            print(form.gender.data)
            return redirect("/")


    return render_template("sign_up.html", form=form)



@app.route("/Login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect("/")
        else:
            flash('მითითებული სახელი ან პაროლი არასწორია.')
            return redirect("/Login")
    return render_template("Login.html", form=form)


@app.route("/Logout")
def logout():
    logout_user()
    return redirect("/")



@app.route("/Test")
def test():
    return render_template("test.html", Series=Series)