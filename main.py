from flask import Flask, render_template, request
import requests
import smtplib
import os

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

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
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        message = request.form["message"]
        with smtplib.SMTP(host='smtp.gmail.com') as connection:
            connection.starttls()
            connection.login(user=EMAIL, password=PASSWORD)
            connection.sendmail(from_addr=email,
                                to_addrs=EMAIL,
                                msg=f"Subject:from {name}-{phone}!\n\n{message}")
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
