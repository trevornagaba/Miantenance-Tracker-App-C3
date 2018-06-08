from flask import Flask, request, jsonify
import json
from myapp import app
from myapp.models import DB
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps

app.config['SECRET KEY'] = 'thisissecret'

database = DB()


class Auth():
    def token_required(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if 'x-access-token' in request.headers:
                token = request.headers['x-access-token']
            else:
                return jsonify(
                    {
                        'message': 'Token is missing, you have not logged in'
                    }
                )
            try:
                data = jwt.decode(token, str(app.config['SECRET_KEY']))
                current_user = database.get_user_byid(data['id'])
            except:
                return jsonify(
                    {
                        'message': 'Token is invalid. Please log in.'
                    }
                )
            return f(current_user, *args, **kwargs)
        return decorated

    # Register a user

    @app.route('/v1/auth/signup', methods=['POST'])
    def signup():
        # Retrieve the data
        data = request.get_json()
        hashed_password = generate_password_hash(
            data['password'], method='sha256')
        # Validate the data
        if not data['username'].strip(" ") or not data['password'].strip(" ") or not data['reenter_password'].strip(" "):
            return jsonify(
                {
                    'message': 'One of the required fields is missing.'
                }
            ), 400
        if data['password'] != data['reenter_password']:
            return jsonify(
                {
                    'message': 'Your passwords do not match'
                }
            ), 400
        if data['username'].isalnum() == False or data['password'].isalnum() == False or data['reenter_password'].isalnum() == False:
            return jsonify(
                {
                    'status': 'FAILED',
                    'message': 'Invalid input. Check for symbols'
                }
            ), 400

        # Catch Type error if username does not exist in db.
        try:
            user_name = database.get_user_byname(data['username'])
            if user_name['username'] == data['username']:
                return jsonify(
                    {
                        'status': 'FAILED',
                        'message': 'Invalid username'
                    }
                ), 400
        except:
            database.add_user(data['username'], hashed_password)
            return jsonify(
                {
                    'status': 'OK',
                    'message': 'User registered',
                    'username': database.get_user_byname(data['username'])
                }
            ), 201

    # Login a user

    @app.route('/v1/auth/login', methods=['POST'])
    def login():

        data = request.get_json()

        if not data['username'].strip(" ") or not data['password'].strip(" "):
            return jsonify(
                {
                    'message': 'One of your login fields is missing.'
                }
            ), 400
        try:
            my_user = database.get_user_byname(data['username'])
            if check_password_hash(my_user['password'], data['password']):
                token = jwt.encode({'id': my_user['id'], 'exp': datetime.datetime.utcnow(
                ) + datetime.timedelta(minutes=30)}, str(app.config['SECRET_KEY']))
                return jsonify(
                    {
                        'token': token.decode('UTF-8'),
                        'user': my_user
                    }
                ), 201
            return jsonify(
                {
                    'message': 'Could not verify. Please check your login details'
                }
            ), 400
        except:
            return jsonify(
                {
                    'message': 'Could not verify, no user found'
                }
            ), 400
