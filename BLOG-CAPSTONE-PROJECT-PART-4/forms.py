from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from wtforms import StringField, EmailField, SubmitField, PasswordField
from wtforms.validators import DataRequired, URL


##WTForm
# New Post
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


# New User
class RegisterForm(FlaskForm):
    email = EmailField(label='Email', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    name = StringField(label='Name', validators=[DataRequired()])
    submit = SubmitField(label="Sign me UP!")


# New Login
class LoginForm(FlaskForm):
    email = EmailField(label='Email', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Log in!')

