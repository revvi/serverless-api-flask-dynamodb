# app.py

from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello and welcome!"

@app.route("/ping")
def ping():
    return "You gave ping! I will give you ping pong!"

