import flask
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import CreatePostForm, RegisterForm, LoginForm, CommentForm  # External File
from functools import wraps
from flask_gravatar import Gravatar

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)
gravatar = Gravatar(app, size=100, rating='g', default='retro', force_default=False, force_lower=False, use_ssl=False, base_url=None)


# Create admin-only decorator
def admin_only(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        # if id is not 1 then return abort with 403 error
        if current_user.id != 1:
            return flask.abort(403)
        else:
            # Otherwise continue with the route function
            return func(*args, **kwargs)
    return decorated_function


## LOGIN SESSION
login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##CONFIGURE TABLES
with app.app_context():
    # Users
    class User(UserMixin, db.Model):
        __tablename__ = "users"
        id = db.Column(db.Integer, primary_key=True)
        email = db.Column(db.String(250), nullable=False)
        password = db.Column(db.String, nullable=False)
        name = db.Column(db.String(50), nullable=False)

        # This will act like a List of BlogPost objects attached to each User.
        # The "author" refers to the author property in the BlogPost class.
        posts = db.relationship("BlogPost", back_populates="author")  # Child

        # This will act like a List of Comments in BlogPosts May exist.
        # "comment_author" refers to the comment_author property in the Comment class.
        comments = db.relationship("Comment", back_populates="comment_author")

    # Posts
    class BlogPost(db.Model):
        __tablename__ = "blog_posts"
        id = db.Column(db.Integer, primary_key=True)

        # Create Foreign Key, "users.id" the users refers to the tablename of User.
        author_id = db.Column(db.Integer, ForeignKey('users.id'))
        # Create reference to the User object, the "posts" refers to the posts protperty in the User class.
        author = db.relationship("User", back_populates="posts")

        title = db.Column(db.String(250), unique=True, nullable=False)
        subtitle = db.Column(db.String(250), nullable=False)
        date = db.Column(db.String(250), nullable=False)
        body = db.Column(db.Text, nullable=False)
        img_url = db.Column(db.String(250), nullable=False)

        # Comments of each BlogPost
        # Child of Parent BlogPost
        comments = db.relationship('Comment', back_populates='parent_post')

    # Comments
    class Comment(db.Model):
        __tablename__ = "comments"

        id = db.Column(db.Integer, primary_key=True)

        # Child Relationship
        # "users.id" The users refers to the tablename of the Users class.
        # "comments" refers to the comments property in the User class.
        author_id = db.Column(db.Integer, ForeignKey("users.id"))
        comment_author = relationship("User", back_populates="comments")

        # Child Relationship
        # Comment of 'what' BlogPost
        # BlogPost is the Parent
        parent_post = db.relationship('BlogPost', back_populates='comments')
        post_id = db.Column(db.Integer, ForeignKey('blog_posts.id'))

        text = db.Column(db.Text, nullable=False)


    db.create_all()



##FLASK ROUTES
@app.route('/')
def get_all_posts():
    posts = db.session.query(BlogPost).all()
    return render_template("index.html", all_posts=posts)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():

        # Search email in the database
        search_result = db.session.query(User).filter_by(email=form.email.data).first()
        if search_result is None:  # if the user does not allready exists
            # Add new user to DataBase
            new_user = User(email=form.data.get('email'),
                            # password=form.data.get('password'),
                            password=generate_password_hash(form.data.get('password'), salt_length=8),
                            name=form.data.get('name'))
            db.session.add(new_user)
            db.session.commit()
            # Logs the user in!
            login_user(new_user)
            return redirect(url_for('get_all_posts'))
        else:
            # Return Flash Messsage
            flash("The email is allready in Database, Please Log In!")
            return redirect(url_for('login'))
    return render_template("register.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_trying_to_login = db.session.query(User).filter_by(email=form.email.data).first()
        # If the user Exists
        if user_trying_to_login:
            # Check the password
            if check_password_hash(pwhash=user_trying_to_login.password,
                                   password=form.password.data):
                # Login the User!
                login_user(user_trying_to_login)
                flash('You are succesfully Logged In!')
                return redirect(url_for('login'))
            else:
                flash('The password is not correct!')
                return redirect(url_for('login'))
        else:
            flash('The email does not exists!')
            return redirect(url_for('login'))

    return render_template("login.html", form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))


@app.route("/post/<int:post_id>", methods=["GET", "POST"])
def post_page(post_id):

    # BlogPost
    requested_post = db.session.query(BlogPost).get(post_id)

    # All comments on this BlogPost
    all_comments = db.session.query(Comment).filter_by(post_id=post_id).all()

    # Create a comment
    form = CommentForm()
    if form.validate_on_submit():
        # If user is not logged in, reroute him to the login page with a flash to log in
        if not current_user.is_active:
            flash("Please Log In, to be able to Comment")
            return redirect(url_for("login"))
        new_comment = Comment(
            author_id=current_user.id,
            comment_author=current_user,
            parent_post=requested_post,
            post_id=post_id,
            text=request.form.get('comment')
        )
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for("post_page", post_id=post_id))

    return render_template("post.html", post=requested_post, form=form, all_comments=all_comments)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/new-post", methods=["GET", "POST"])
@login_required
@admin_only
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user,
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form)


@app.route("/edit-post/<int:post_id>")
@login_required
@admin_only
def edit_post(post_id):
    post = BlogPost.query.get(post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = edit_form.author.data
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))

    return render_template("make-post.html", form=edit_form)


@app.route("/delete/<int:post_id>")
@login_required
@admin_only
def delete_post(post_id):
    post_to_delete = BlogPost.query.get(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
