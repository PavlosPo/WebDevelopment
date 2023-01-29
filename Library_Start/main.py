from flask import Flask, render_template, request, redirect, url_for
import sqlite3


app = Flask(__name__)
all_books = []


db = sqlite3.connect("books-collection.db")
cursor = db.cursor()  # It modifies, creates, interact with the files
cursor.execute("CREATE TABLE books (id INTEGER PRIMARY KEY, title varchar(250) NOT NULL UNIQUE, author varchar(250) NOT NULL, rating FLOAT NOT NULL)")


@app.route('/')
def home():
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
        current_book_dictionary = {'title': request.form.get('book'), 'author': request.form.get('book_author'),
                                   'rating': request.form.get('rating')}
        all_books.append(current_book_dictionary)
        return redirect(url_for('home'))
    else:
        return render_template('add.html')


if __name__ == "__main__":
    app.run(debug=True)

