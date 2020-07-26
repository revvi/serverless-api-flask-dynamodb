# app.py

from flask import Flask, render_template
app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello world!"


@app.route("/ping")
def ping():
    return { "message": "You gave ping! I will give you ping pong!" }


@app.route("/lipsum")
def go():
    return render_template("index.html")
