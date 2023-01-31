from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
import sqlite3
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-books-collection.db"
db = SQLAlchemy(app)

# db = sqlite3.connect("books-collection.db")
# cursor = db.cursor()  # It modifies, creates, interact with the files
# cursor.execute("CREATE TABLE books (id INTEGER PRIMARY KEY, title varchar(250) NOT NULL UNIQUE, author varchar(250) NOT NULL, rating FLOAT NOT NULL)")
# cursor.execute("INSERT INTO books VALUES(1, 'Harry Potter', 'J. K. Rowling', '9.3')")
# db.commit()

with app.app_context():
    class Book(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(250), nullable=False, unique=True)
        author = db.Column(db.String(250), nullable=False)
        rating = db.Column(db.Float(), nullable=False)

        def __init__(self, title, author, rating):
            self.title = title
            self.author = author
            self.rating = rating

        def __repr__(self):
            return '<User %r>' % self.title

    # db.create_all()
    # new_book = Book(id=2, title="Harry Potter", author="J. K. Rowling", rating=9.3)
    # db.session.add(new_book)
    # db.session.commit()


class BooksForm(FlaskForm):
    title = StringField("Book's Name", validators=[DataRequired()])
    author = StringField("Book's Author", validators=[DataRequired()])
    rating = StringField("Book's Rating", validators=[DataRequired()])
    submit = SubmitField('Submit')


# Flask Section
@app.route('/')
def home():
    all_books = db.session.query(Book).all()
    if len(all_books) == 0:
        empty_list_of_books = True
    else:
        empty_list_of_books = False
    return render_template('index.html',
                           all_books=all_books,
                           empty_list_of_books=empty_list_of_books)


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # current_book_dictionary = {'title': request.form.get('book'), 'author': request.form.get('book_author'),
        #                            'rating': request.form.get('rating')}
        book_to_add = Book(title=request.form.get('book'),
                           author=request.form.get('book_author'),
                           rating=request.form.get('rating'))
        db.session.add(book_to_add)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        return render_template('add.html')


@app.route('/change_rating/<id>', methods=['GET', 'POST'])
def change_rating(id):
    current_book = db.session.query(Book).filter_by(id=id).first()
    if request.method == 'GET':
        return render_template('changing_rating.html', book=current_book)
    if request.method == "POST":
        new_rating = request.form.get('new_rating')
        current_book.rating = new_rating
        db.session.commit()
        return redirect(url_for('home'))


@app.route('/delete')
def delete():
    book_id = request.args.get('id')
    # DELETE A RECORD BY ID
    book_to_delete = Book.query.get(book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
