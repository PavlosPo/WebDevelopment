from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, IntegerRangeField, FloatField
from wtforms.validators import DataRequired
import requests
import os

API_KEY = 'a97e7b4324e3a41952e5a62fb05b41f3'

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
db = SQLAlchemy(app)


# API for data extraction after adding or searching a movie
def search_movie(movie_title=None, movie_id=None):
    """If Movie title is given, it finds all the results,
    else if Id of a Movie is given, it returns all the data of that movie id"""

    if movie_id is None and movie_title is not None:
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
    elif (movie_id is not None) and (movie_title is None):
        API_ENDPOINT = f'https://api.themoviedb.org/3/movie/{movie_id}'
        params = {
            'api_key': API_KEY
        }
        response = requests.get(url=API_ENDPOINT, params=params)
        response.raise_for_status()
        data = response.json()
        print(data)
        return data
    else:
        print('You can not enter Both Movie Title and Movie Id. You are on different functionalities.')
        return 0


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
        api_id = db.Column(db.Integer, nullable=True)

        def __init__(self, title, year, description, rating, ranking, review, img_url, api_id=None):
            self.title = title
            self.year = year
            self.description = description
            self.rating = rating
            self.ranking = ranking
            self.review = review
            self.img_url = img_url
            self.api_id = api_id


    db.create_all()


# Form to Update Rating or Review
class RateMovieForm(FlaskForm):  # Form
    new_rating = FloatField(label="Your Rating Out of 10 e.g. 7.5", validators=[DataRequired()])
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
    # Query the movies based on rating ( Higher to Lower )
    movie_table = Movie.query.order_by(Movie.rating.desc()).all()  # Get the Movie Table in order by rating desc
    # Render the movies
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
        movie.review = form.new_review.data
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
        # Data are fetched from an API
        data = search_movie(movie_title=movie_to_find)['results']
        return render_template('select.html', options=data)
    return render_template('add.html', form=form)


# Fetch Movie Data and Add this to DataBase
@app.route('/fetch_data/')
def fetch_movie_data_and_add():
    movie_to_add_api_id = request.args.get('movie_selected_id')
    movie_to_add_data = search_movie(movie_id=movie_to_add_api_id)
    movie_to_add = Movie(
        title=movie_to_add_data['title'],
        year=movie_to_add_data['release_date'].split("-")[0],
        description=movie_to_add_data['overview'],
        review='None',  # We initializing as None
        rating=0,  # Initializing as 0
        ranking=movie_to_add_data['vote_average'],
        img_url='https://image.tmdb.org/t/p/original' + str(movie_to_add_data['poster_path']),
        api_id=movie_to_add_api_id  # We add this so we can relation this new movie with our datbase later
    )

    db.session.add(movie_to_add)
    db.session.commit()

    # Read the movie id that was assigned to the new movie in our datbase,
    # and push it to the update page so we can add a review and rating
    resently_added_movie = db.session.query(Movie).filter_by(api_id=movie_to_add_api_id).first()
    # Redirect the recently added movie for an update in rating, review with the id got from the database
    return redirect(url_for('update', movie_id=resently_added_movie.id))


if __name__ == '__main__':
    app.run(debug=True)
