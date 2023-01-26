from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email


app = Flask(__name__)

app.config["SECRET_KEY"] = '5f18d396d4038e7b684543b2f2b79af4'


# Class for Flask WTForms
class Form(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    email = StringField('email', validators=[Email()])
    message = TextAreaField('message', validators=[DataRequired()])
    send = SubmitField('send')


@app.route("/")
def home():
    # Create the Form Class and form object to pass it into the HTML file
    form = Form()
    return render_template('index.html', form=form)


@app.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
