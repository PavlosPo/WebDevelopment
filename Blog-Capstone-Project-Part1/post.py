import requests


class Post:

    def __init__(self):
        self.posts = []
        self.blog_titles = []
        self.blog_bodies = []
        self.blog_subtitles = []
        self.get_posts_from_api()  # Retrives information

    def get_posts_from_api(self):
        api_endpoint = "https://api.npoint.io/c790b4d5cab58020d391"
        response = requests.get(url=api_endpoint)
        response.raise_for_status()
        blog_posts = response.json()  # Returns a list of json files
        self.posts = blog_posts
        self.blog_titles = [post['title'] for post in blog_posts]
        self.blog_bodies = [post['body'] for post in blog_posts]
        self.blog_subtitles = [post['subtitle'] for post in blog_posts]
