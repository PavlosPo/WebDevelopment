from flask import Flask
import random

app = Flask(__name__)


# Decorator Make Bold
def make_bold(function):
    def wrapper():
        return f"<b>" + function() + "</b>"
    return wrapper


# Decorator Make Emphasis
def make_emphasis(function):
    def wrapper():
        return f"<em>" + function() + "</em>"
    return wrapper


# Decorator Make Underlined
def make_underlined(function):
    def wrapper():
        return f"<u>" + function() + "</u>"
    return wrapper


@app.route("/username/<name>/<int:number>")
def greet(name, number):
    return f"Hello there {name}, you are {number} years old"


@app.route("/")  # When we are navigating to route dir
def hello_world():
    return '<h1 style="text-align: center">Hello, World</h1>' \
           '<p>This is a paragraph</p>' \
           '<img src="https://giphy.com/clips/hamlet-cat-kitten-meow-2DtyNDEi72HAYWj3uo">'


@app.route("/bye")
@make_bold
@make_emphasis
@make_underlined
def say_bye():
    return "Bye"


if __name__ == "__main__":  # We are running the code within this file
    app.run(debug=True)
