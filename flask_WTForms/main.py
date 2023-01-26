from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo


app = Flask(__name__)

app.secret_key = '5f18d396d4038e7b684543b2f2b79af4'


# Class for Flask WTForms
class Form(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired(),
                                                   Email()])
    password = PasswordField(label='Password', validators=[DataRequired(),
                                                           Length(min=8)])
    submit = SubmitField(label="Login")


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    # Create the Form Class and form object to pass it into the HTML file
    login_form = Form()

    # If we have a POST Request or else the form is making a submit then print data
    if login_form.validate_on_submit():  # If submited AND validated AND Credentials match then True
        correct_email = "admin@email.com"
        correct_password = "12345678"
        # If correct email credentials
        if login_form.data['email'] == correct_email and login_form.data['password'] == correct_password:
            return render_template('success.html')
        else:
            return render_template('denied.html')
    return render_template('login.html', form=login_form)


if __name__ == '__main__':
    app.run(debug=True)
