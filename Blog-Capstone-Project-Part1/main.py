from flask import Flask, render_template
from post import Post

app = Flask(__name__)


@app.route('/')
def home():
    blog_posts = Post()
    info_to_pass = blog_posts.posts
    return render_template("index.html",
                           posts=info_to_pass)


@app.route("/post/<int:blog_id>")
def blog_posts_page(blog_id):
    blog_posts = Post()
    current_post = [post for post in blog_posts.posts if post['id'] == blog_id][0]
    print(current_post)
    return render_template("post.html",
                           blog_post_to_show=current_post)


if __name__ == "__main__":
    app.run(debug=True)
