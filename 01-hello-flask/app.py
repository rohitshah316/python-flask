from flask import Flask

app=Flask(__name__)

@app.route("/")
def home():
    return "Hello, flask"

@app.route("/about")
def about():
    return "This is about page"


@app.route("/hello/<name>")
def hello(name):
    return f"Hello, named {name}."

@app.route("/contact")
def contact():
    return "Contact me at: hello@example.com"