from flask import Flask, render_template, url_for
import requests
import datetime
app = Flask(__name__)
api_endpoint = "https://api.npoint.io/f8151ab1f10f7e9cf7a8"


def api_brain():
    response = requests.get(url=api_endpoint)
    response.raise_for_status()
    data = response.json()
    return data

@app.route("/")
def home_page():
    data = api_brain()
    current_date = datetime.datetime.now()
    return render_template("index.html",
                           data=data,
                           month=current_date.strftime("%B"),
                           day_of_date=current_date.day,
                           year_of_date=current_date.year)


@app.route("/about")
def about_page():
    return render_template("about.html")


@app.route("/contact")
def contact_page():
    return render_template("contact.html")


@app.route("/post/<id>")
def create_post_page(id):
    return render_template("post.html",
                           post_id=id)


if __name__ == "__main__":
    app.run(debug=True)
