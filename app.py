# app.py
import os
from flask import Flask, Blueprint, render_template

# init flask application
app = Flask(__name__)

# get base path based on BASE_PATH in serverless.yml
base_path = "/" + os.environ.get('BASE_PATH')
bp = Blueprint('application', __name__, url_prefix=base_path)


@bp.route("/")
def hello():
    return "This is POC service from magerabis"


@bp.route("/pingpong")
def ping():
    return {"message": "You gave ping! I will give you ping pong!"}


@bp.route("/lipsum")
def lipsum():
    return render_template("index.html")


# register blueprint
app.register_blueprint(bp)
