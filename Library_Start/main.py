from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import os
basedir = os.path.abspath(os.path.dirname(__file__))


def create_app():
    app = Flask(__name__)

    with app.app_context():
        init_db()

    return app

app = create_app()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
db = SQLAlchemy(app)
all_books = []


# db = sqlite3.connect("books-collection.db")
# cursor = db.cursor()  # It modifies, creates, interact with the files
# cursor.execute("CREATE TABLE books (id INTEGER PRIMARY KEY, title varchar(250) NOT NULL UNIQUE, author varchar(250) NOT NULL, rating FLOAT NOT NULL)")
# cursor.execute("INSERT INTO books VALUES(1, 'Harry Potter', 'J. K. Rowling', '9.3')")
# db.commit()

class Library(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False, unique=True)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float(), nullable=False)

    def __init__(self, id, title, author, rating):
        db.drop_all()
        self.id = id
        self.title = title
        self.author = author
        self.rating = rating
        db.create_all()



@app.route('/')
def home():
    if len(all_books) == 0:
        empty_list_of_books = True
    else:
        empty_list_of_books = False
    test_data = Library('Hary Potter', 'J. K. Rowling', 9.3)
    db.session.add(test_data)
    db.session.commit()
    return render_template('index.html',
                           all_books=all_books,
                           empty_list_of_books=empty_list_of_books)


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        current_book_dictionary = {'title': request.form.get('book'), 'author': request.form.get('book_author'),
                                   'rating': request.form.get('rating')}
        all_books.append(current_book_dictionary)
        return redirect(url_for('home'))
    else:
        return render_template('add.html')


if __name__ == "__main__":
    db.drop_all()
    db.create_all()
    app.run(debug=True)

