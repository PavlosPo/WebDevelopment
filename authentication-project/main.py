from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user


app = Flask(__name__)



app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

## Login Session Init
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


## CREATE TABLE IN DB
with app.app_context():
    class User(UserMixin, db.Model):
        id = db.Column(db.Integer, primary_key=True)
        email = db.Column(db.String(100), unique=True)
        password = db.Column(db.String(100))
        name = db.Column(db.String(1000))

        # Line below only required once, when creating DB.
        # db.create_all()


## Form To Register User
class RegisterForm(FlaskForm):
    email = StringField(label="Email", validators=[DataRequired(), Email()])
    name = StringField(label="Name", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    submit = SubmitField()


## Form to Login The User
class LoginForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Login In')





## Flask Section
@app.route('/')
def home():
    return render_template("index.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    global current_user
    # register_form = RegisterForm()
    # if register_form.validate_on_submit():
    #     print("Sucess")
    # return render_template("register.html", form=register_form)
    if request.method == "POST":
        current_email = request.form.get('email')
        current_password_secured = generate_password_hash(
            request.form.get('password'),
            method="pbkdf2:sha256",
            salt_length=8)
        new_user = User(name=request.form.get('name'),
                        email=current_email,
                        password=current_password_secured)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('secrets'))
    return render_template('register.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        # Find user by email entered.
        user = User.query.filter_by(email=email).first()

        # Check stored password hash against entered password hashed.
        if check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('secrets'))


    # # Check the form is submited to login
    # if request.method == ["POST"]:
    #     # Finds the user who is trying to login
    #     try:
    #         user_email = request.args.get('email')
    #         user_trying_to_login_in = db.session.query(User).filter_by(email=user_email).first()
    #
    #         # If the user exists continues to identify the password
    #         try:
    #             hashed_password = db.session.query(User.password).get(user_trying_to_login_in.id)
    #             given_password = request.args.get('password')
    #             # If all is fine then it logs in the user and saves the session of that user
    #             try:
    #                 # if password it's okey
    #                 if check_password_hash(pwhash=hashed_password, password=given_password):
    #                     # Logs the user in
    #                     login_user(user_trying_to_login_in)
    #                     print('You are connected!!')
    #                     return redirect(url_for('secrets'))
    #             except:
    #                 return render_template("<p>Something went wrong logging in the user. All the validations are checked though! :/</p>")
    #         except:
    #             return render_template("<p>The password is not correct !</p>")
    #     except:
    #         return render_template("<p>The User does not exists !</p>")

    return render_template("login.html")


@app.route('/secrets')
@login_required
def secrets():
    name = current_user.name
    return render_template("secrets.html", user_name=name)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/download', methods=["GET"])
@login_required
def download():
    return send_from_directory('static', path='/files/cheat_sheet.pdf')


if __name__ == "__main__":
    app.run(debug=True)
