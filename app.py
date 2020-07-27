# app.py
import os
import boto3
from flask import Flask, Blueprint, render_template, jsonify, request

# init flask application
app = Flask(__name__)

# set table name for dynamodb
USERS_TABLE = os.environ.get('USERS_TABLE')

# check if this runs locally via serverless-wsgi
IS_OFFLINE = os.environ.get('IS_OFFLINE')

if IS_OFFLINE:
    client = boto3.client(
        'dynamodb',
        region_name='localhost',
        endpoint_url='http://localhost:8000'
    )
else:
    client = boto3.client('dynamodb')

# get base path based on BASE_PATH in serverless.yml
BASE_PATH = "/" + os.environ.get('BASE_PATH')
bp = Blueprint('application', __name__, url_prefix=BASE_PATH)


@bp.route("/")
def hello():
    return "This is POC service from magerabis"


@bp.route("/pingpong")
def ping():
    return {"message": "You gave ping! I will give you ping pong!"}


@bp.route("/lipsum")
def lipsum():
    return render_template("index.html")


@bp.route("/users/<string:user_id>")
def get_user(user_id):
    resp = client.get_item(
        TableName=USERS_TABLE,
        Key={
            'userId': {'S': user_id}
        }
    )
    item = resp.get('Item')
    if not item:
        return jsonify({'error': 'User does not exist'}), 404

    return jsonify({
        'userId': item.get('userId').get('S'),
        'name': item.get('name').get('S')
    })


@bp.route("/users", methods=["POST"])
def create_user():
    user_id = request.json.get('userId')
    name = request.json.get('name')
    if not user_id or not name:
        return jsonify({'error': 'Please provide userId and name'}), 400

    resp = client.put_item(
        TableName=USERS_TABLE,
        Item={
            'userId': {'S': user_id},
            'name': {'S': name}
        }
    )

    return jsonify({
        'userId': user_id,
        'name': name
    })


# register blueprint
app.register_blueprint(bp)
