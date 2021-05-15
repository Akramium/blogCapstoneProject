from flask import Flask, render_template, request
import requests

app = Flask(__name__)

posts = requests.get(url="https://api.npoint.io/0067e63917ca7a5034d9").json()


@app.route('/')
def home():
    return render_template('index.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        print(request.form["name"])
        print(request.form["email"])
        return render_template('contact.html', message='Successfully sent message')
    return render_template('contact.html')


@app.route('/post/<int:post_id>')
def post(post_id):
    requested_post = None
    for blog_post in posts:
        if post_id == blog_post["id"]:
            requested_post = blog_post
    return render_template('post.html', post=requested_post)


if __name__ == '__main__':
    app.run(debug=True)
