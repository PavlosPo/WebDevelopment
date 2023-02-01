from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, IntegerRangeField
from wtforms.validators import DataRequired
import requests
import os

API_KEY = os.environ["MOVIE_API_KEY"]

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
db = SQLAlchemy(app)


# API for data extraction after adding or searching a movie
def search_movie(movie_title, movie_id=None):
    """If Movie title is given, it finds all the results,
    else if Id of a Movie is given, it returns all the data of that movie id"""

    if movie_id is None:
        API_ENDPOINT = 'https://api.themoviedb.org/3/search/movie'
        params = {
            'api_key': API_KEY,
            'query': str(movie_title),
            'language': 'en-US'
        }
        response = requests.get(url=API_ENDPOINT, params=params)
        response.raise_for_status()
        data = response.json()
        return data
    else:
        API_ENDPOINT = f'https://api.themoviedb.org/3/search/movie/{movie_id}'
        params = {
            'api_key': API_KEY,
            'language': 'en-US'
        }
        response = requests.get(url=API_ENDPOINT, params=params)
        print(response)
        response.raise_for_status()
        data = response.json()
        print(data)
        return data


# DataBase Initializing
with app.app_context():
    class Movie(db.Model):  # Movie Table
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(50), nullable=False)
        year = db.Column(db.Integer, nullable=False)
        description = db.Column(db.String(250), nullable=True)
        rating = db.Column(db.Float, nullable=False)
        ranking = db.Column(db.Integer, nullable=False)
        review = db.Column(db.String(250), nullable=True)
        img_url = db.Column(db.String, nullable=True)

        def __init__(self, title, year, description, rating, ranking, review, img_url):
            self.id = id
            self.title = title
            self.year = year
            self.description = description
            self.rating = rating
            self.ranking = ranking
            self.review = review
            self.img_url = img_url


    db.create_all()
    ### Import Once this Data
    # new_movie = Movie(
    #     title="Phone Booth",
    #     year=2002,
    #     description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
    #     rating=7.3,
    #     ranking=10,
    #     review="My favourite character was the caller.",
    #     img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg")
    #
    # db.session.add(new_movie)
    # db.session.commit()


# Form to Update Rating or Review
class RateMovieForm(FlaskForm):  # Form
    new_rating = IntegerField(label="Your Rating Out of 10 e.g. 7.5", validators=[DataRequired()])
    new_review = StringField(label='Your Review', validators=[DataRequired()])
    submit = SubmitField(label='Done')


# Form to find and fetch the given movie entered
class FormForMovieFinder(FlaskForm):
    title = StringField(label='Movie Title', validators=[DataRequired()])
    submit = SubmitField(label='Add Movie')


# Flask Section
# Home Page
@app.route("/")
def home():
    movie_table = Movie.query.all()  # Get the Movie Table
    return render_template("index.html", all_movies=movie_table)


# Update Review and Rating
@app.route('/update', methods=['POST', 'GET'])
def update():
    current_movie_id = request.args.get('movie_id')
    # movie = Movie.query.filter_by(id=current_movie_id).all()
    movie = Movie.query.get(current_movie_id)  # It is the same
    form = RateMovieForm()

    if form.validate_on_submit():
        movie.rating = form.new_rating.data
        movie.description = form.new_review.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit.html', movie=movie, form=form)


# Delete Movie
@app.route('/delete')
def delete_movie():
    movie_id = request.args.get('movie_id')
    movie = Movie.query.get(movie_id)
    print(movie)
    db.session.delete(movie)
    db.session.commit()
    print('It is deleted')
    return redirect(url_for('home'))


# Add Movie
@app.route('/add/', methods=['GET', 'POST'])
def add_movie():
    form = FormForMovieFinder()
    if form.validate_on_submit():
        movie_to_find = form.title.data
        data = search_movie(movie_to_find)['results']
        print(data)
        return render_template('select.html', options=data)
    return render_template('add.html', form=form)


# Fetch Movie Data and Add this to DataBase
@app.route('/fetch_data/')
def fetch_movie_data_and_add():

    movie_to_add_id = request.args.get('movie_selected_id')
    print(movie_to_add_id)
    movie_to_add = search_movie(movie_to_add_id)
    print(movie_to_add)
    # db.session.add()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
