from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route("/")
def home_page():
    return render_template("index.html")


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
