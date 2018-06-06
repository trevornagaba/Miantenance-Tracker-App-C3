from flask import Flask, request, jsonify
from myapp.models import Request, User
import json
from myapp import app
from myapp import db
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps

app.config['SECRET KEY'] = 'thisissecret'

requests = Request()
users = User()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message':'Token is missing.'})

        try:
            data = jwt.decode(token, str(app.config['SECRET_KEY']))
            current_user = users.get_user_byid(data['id'])

        except:
            return jsonify({'message':'Token is invalid.'})
        return f(current_user,*args,**kwargs)
    return decorated

# Register a user
@app.route('/v1/auth/signup', methods = ['POST'])
def signup():
    #Retrieve the data
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    # Validate the data
    if not data['username']:
        return jsonify ({ 'message': 'Please enter your username' }), 400
    if not data['password']:
        return jsonify ({'message': 'Please enter your password'}), 400
    if not data['reenter_password']:
        return jsonify ({'message': 'Please re-enter your password'}), 400

    if data['password'] != data['reenter_password']:
        return jsonify ({'message': 'Your passwords do not match'}), 400

    users.add_user(data['username'], hashed_password)
    return jsonify (
        {
            'status': 'OK',
            'message': 'User registered',
            'username': users.get_user_byname(data['username']),
            'number of users': users.number_of_users()
        }
    ), 201

# Login a user
@app.route('/v1/auth/login', methods = ['POST'])
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return jsonify ({'message': 'Could not verify, login required'})
    
    my_user = users.get_user_byname(auth.username)

    if not my_user:
        return jsonify({'message': 'Could not verify, no user found'})

    if check_password_hash(my_user['password'], auth.password):
        token = jwt.encode({'id': my_user['id'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, str(app.config['SECRET_KEY']))
        return jsonify(
            {
                'token' : token.decode('UTF-8'),
                'users': users.get_all_users(),
                'user' : my_user
                }
        )

    return jsonify({'message': 'Could not verify, login required...'})

#Create a request
@app.route('/v1/users/requests', methods = ['POST'])
@token_required
def create_requests(current_user):
    # Retrieve the data
    data = request.get_json()
    # Validate the data
    if data['device_type'] == "" or data['fault_description'] == "":
        return jsonify (
            {
                'status': 'FAILED',
                'message': 'One of the required fields is empty'
        }
        ), 400
    try:
        if isinstance(data['device_type'].encode(), str) and isinstance (data['fault_description'].encode(), str):
            # Create id and store the data
            _request = requests.add_request(current_user['id'], data['device_type'], data['fault_description'])
            id = _request[1]
            return jsonify(
                {
                    'status':'OK',
                    'message': 'Request created successfully',
                    'device-status': requests.get_request(id)['device_status'],
                    'device-type': requests.get_request(id)['device_type'],
                    'request-id': requests.get_request(id)['id']
                }
            ), 201
    except AttributeError:
        return jsonify(
            {
                'status':'FAILED',
                'message': 'Invalid request. Please check your entry',
            }
        ), 400

#Fetch all requests of a logged in user
@app.route('/v1/users/requests', methods = ['GET'])
@token_required
def view_requests(current_user):
    if requests.number_of_requests < 1:
        return jsonify(
            {
                'status':'FAILED',
                'message': 'No requests added',
            }
        ), 400
    return jsonify(
            {
            'status':'OK', 
            'message':'successful',
            'requests': requests.get_user_requests(current_user['id']) 
            }
        ), 200
        

#Fetch a request that belongs to a logged in user
@app.route('/v1/users/requests/<id>', methods = ['GET'])
@token_required
def view_user_requests(current_user, id):
    try:     
        # Validate request
        return jsonify(
            {
            'status':'OK', 
            'message':'successful',
            'device-type': requests.get_request(id)['device_type'],
            'fault description': requests.get_request(id)['fault_description'],
            'device-status': requests.get_request(id)['device_status'],
            'id': requests.get_request(id)['id']
            }
        ), 200
    # Catch none integer input
    except  ValueError:
        return jsonify(
            {
                'status':'FAILED',
                'message':'Invalid request id'
            }
        ), 400
    # Catch request for non-existent id
    except IndexError:
        return jsonify(
            {
                'status':'FAILED',
                'message':'Your request id does not exist'
            }
        ), 400

#Modify a request
@app.route('/v1/users/requests/<id>', methods = ['PUT'])
@token_required
def modify_requests(current_user, id):
    # Retrieve the request
    data = request.get_json()
    # Validate the data
    if data['device_type'] == "" or data['fault_description'] == "":
        return jsonify (
            {
                'status': 'OK',
                'message': 'One of the required fields is empty'
        }
        )
    try:
        if isinstance(data['device_type'].encode(), str) and isinstance(data['fault_description'].encode(), str):
            # Store the data 
            user_id = requests.get_request(id)['user_id']
            if current_user['id'] == user_id:
                if not requests.get_request(id):
                    return jsonify(
                        {
                            'status': 'FAILED',
                            'message': 'Invalid request id. Id does not match any of your requests.'
                        }
                    )
                _request = requests.modify_request(id, data['device_type'], data['fault_description'])
                _id = _request[1]
                return jsonify(
                    {
                        'status': 'OK',
                        'device-type': requests.get_request(_id)['device_type'],
                        'fault-description': requests.get_request(_id)['fault_description'],
                        'message': 'A request was modified',
                        'request-id': requests.get_request(_id)['id'],
                        'device-status': requests.get_request(_id)['device_status']
                    }
                ), 200    
            return jsonify(
                {
                    'status': 'FAILED',
                    'message': 'Invalid request id. Id does not match any of your requests.'
                }
            )
    except AttributeError:
        return jsonify(
            {
            'status': 'FAIL',
            'message': 'Failed to modify a request. Data is invalid'
            }
        ), 400

#Admin fetch all requests of all users
@app.route('/v1/requests', methods = ['GET'])
@token_required
def admin_view_requests(current_user):
    #Test if admin
    user = users.get_user_byid(current_user['id'])
    ## Add test for requests in db
    if user['admin'] == False:
        return jsonify(
            {
                'status':'FAILED',
                'message': 'You do not have these permissions',
            }
        ), 400
    return jsonify(
            {
            'status':'OK', 
            'message':'successful',
            'requests': requests.get_all_requests() 
            }
        ), 200

#Admin approve a request
@app.route('/v1/requests/<id>/approve', methods = ['PUT'])
@token_required
def admin_approve_request(current_user, id):
    # Retrieve user
    user = users.get_user_byid(current_user['id'])
    # Test if admin
    if user['admin'] == True:
        if not requests.get_request(id):
            return jsonify(
                {
                    'status': 'FAILED',
                    'message': 'Invalid request id. Id does not match any of your requests.'
                }
            )
        _request = requests.modify_status(id, 'Approved')
        _id = _request[1]
        return jsonify(
            {
                'status': 'OK',
                'device-type': requests.get_request(_id)['device_type'],
                'fault-description': requests.get_request(_id)['fault_description'],
                'message': 'A request was modified',
                'request-id': requests.get_request(_id)['id'],
                'device-status': requests.get_request(_id)['device_status']
            }
        ), 200
    return jsonify (
            {
                'status': 'FAILED',
                'message': 'Access denied. Your do not have these rights.'
        }
        ), 400

#Admin disapprove a request
@app.route('/v1/requests/<id>/disapprove', methods = ['PUT'])
@token_required
def admin_disapprove_request(current_user, id):
    # Retrieve user
    user = users.get_user_byid(current_user['id'])
    # Test if admin
    if user['admin'] == True:
        if not requests.get_request(id):
            return jsonify(
                {
                    'status': 'FAILED',
                    'message': 'Invalid request id. Id does not match any of your requests.'
                }
            )
        _request = requests.modify_status(id, 'Disapproved')
        _id = _request[1]
        return jsonify(
            {
                'status': 'OK',
                'device-type': requests.get_request(_id)['device_type'],
                'fault-description': requests.get_request(_id)['fault_description'],
                'message': 'A request was modified',
                'request-id': requests.get_request(_id)['id'],
                'device-status': requests.get_request(_id)['device_status']
            }
        ), 200
    return jsonify (
            {
                'status': 'FAILED',
                'message': 'Access denied. Your do not have these rights.'
        }
        ), 400

#Admin resolve a request
@app.route('/v1/requests/<id>/resolve', methods = ['PUT'])
@token_required
def admin_resolve_request(current_user, id):
    # Retrieve user
    user = users.get_user_byid(current_user['id'])
    # Test if admin
    if user['admin'] == True:
        if not requests.get_request(id):
            return jsonify(
                {
                    'status': 'FAILED',
                    'message': 'Invalid request id. Id does not match any of your requests.'
                }
            )
        _request = requests.modify_status(id, 'Resolved')
        _id = _request[1]
        return jsonify(
            {
                'status': 'OK',
                'device-type': requests.get_request(_id)['device_type'],
                'fault-description': requests.get_request(_id)['fault_description'],
                'message': 'A request was modified',
                'request-id': requests.get_request(_id)['id'],
                'device-status': requests.get_request(_id)['device_status']
            }
        ), 200
    return jsonify (
            {
                'status': 'FAILED',
                'message': 'Access denied. Your do not have these rights.'
        }
        ), 400