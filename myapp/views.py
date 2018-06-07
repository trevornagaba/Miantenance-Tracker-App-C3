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

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        else:
            return jsonify(
                {
                    'message':'Token is missing, you have not logged in'
                }
            )
        try:
            data = jwt.decode(token, str(app.config['SECRET_KEY']))
            current_user = database.get_user_byid(data['id'])
        except:
            return jsonify(
                {
                    'message':'Token is invalid. Please log in.'
                }
            )
        return f(current_user,*args,**kwargs)
    return decorated

# Register a user
@app.route('/v1/auth/signup', methods = ['POST'])
def signup():
    #Retrieve the data
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    # Validate the data
    if not data['username'] or not data['password'] or not data['reenter_password']:
        return jsonify (
            {
                'message': 'One of the required fields is missing.' 
            }
        ), 400
    if data['password'] != data['reenter_password']:
        return jsonify (
            {
                'message': 'Your passwords do not match'
                }
        ), 400

    # Catch Type error is username does not exist in db and excecute signup when error is caught.
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
        return jsonify (
            {
                'status': 'OK',
                'message': 'User registered',
                'username': database.get_user_byname(data['username'])
            }
        ), 201

# Login a user
@app.route('/v1/auth/login', methods = ['POST'])
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return jsonify ({'message': 'One of your login fields is missing.'}), 400
    
    # Catch type error if username does not exist in database
    try:
        my_user = database.get_user_byname(auth.username)
        if check_password_hash(my_user['password'], auth.password):
            token = jwt.encode({'id': my_user['id'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, str(app.config['SECRET_KEY']))
            return jsonify(
                {
                    'token' : token.decode('UTF-8'),
                    'users': database.get_all_users(),
                    'user' : my_user
                    }
            ), 201
        return jsonify(
            {
                'message': 'Could not verify. Please check your login details'
                }
        ) , 400
    except:
        return jsonify(
            {
                'message': 'Could not verify, no user found'
                }
        ), 400

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
            _request = database.add_request(current_user['id'], data['device_type'], data['fault_description'])
            id = _request['id']
            return jsonify(
                {
                    'status':'OK',
                    'message': 'Request created successfully',
                    'device-status': database.get_request(id)['device_status'],
                    'device-type': database.get_request(id)['device_type'],
                    'request-id': database.get_request(id)['id']
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
    try:
        return jsonify(
            {
            'status':'OK', 
            'message':'successful',
            'requests': database.get_user_requests(current_user['id']) 
            }
        ), 200
    except:
        return jsonify(
            {
                'status':'FAILED',
                'message': 'No requests added',
            }
        ), 400

#Fetch a request that belongs to a logged in user
@app.route('/v1/users/requests/<id>', methods = ['GET'])
@token_required
def view_user_requests(current_user, id):
    # Catch request for an id that does not exist in db
    try: 
        # Test if correct user
        request = database.get_request(id)
        if request['user_id'] == current_user['id']:     
            # Validate request
            return jsonify(
                {
                'status':'OK', 
                'message':'successful',
                'device-type': database.get_request(id)['device_type'],
                'fault description': database.get_request(id)['fault_description'],
                'device-status': database.get_request(id)['device_status'],
                'id': database.get_request(id)['id']
                }
            ), 200
        return jsonify(
                    {
                        'status':'FAILED',
                        'message':'You do not have access to this request.'
                    }
                ), 400
    except:
        return jsonify(
            {
                'status':'FAILED',
                'message':'This request does not exist'
            }
        ), 400

#Modify a request
@app.route('/v1/users/requests/<id>', methods = ['PUT'])
@token_required
def modify_requests(current_user, id):
    # Test if status is approved
    try:
        modify_request = database.get_request(id)
        if modify_request['device_status'] ==  'Approved':
            return jsonify (
                {
                    'status': 'FAILED',
                    'message': 'This request cannot be modified at this time. It has already been approved.'
            }
            ), 400
        if modify_request['user_id'] == current_user['id']:
            return jsonify (
                {
                    'status': 'FAILED',
                    'message': 'Access denied. This request belongs to another user.'
            }
            ), 400
    except:
        return jsonify (
                {
                    'status': 'FAILED',
                    'message': 'This request does not exist.'
            }
            ), 400        
    # Retrieve the request
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
        if isinstance(data['device_type'].encode(), str) and isinstance(data['fault_description'].encode(), str):
            # Store the data 
            _request = database.modify_request(id, data['device_type'], data['fault_description'])
            _id = _request['id']
            return jsonify(
                {
                    'status': 'OK',
                    'device-type': database.get_request(_id)['device_type'],
                    'fault-description': database.get_request(_id)['fault_description'],
                    'message': 'A request was modified',
                    'request-id': database.get_request(_id)['id'],
                    'device-status': database.get_request(_id)['device_status']
                }
            ), 200
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
    user = database.get_user_byid(current_user['id'])
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
            'requests': database.get_all_requests() 
            }
        ), 200

#Admin approve a request
@app.route('/v1/requests/<id>/approve', methods = ['PUT'])
@token_required
def admin_approve_request(current_user, id):
    try:
        # Retrieve user
        user = database.get_user_byid(current_user['id'])
        # Test if admin
        if user['admin'] == True:
            approve_request = database.get_request(id)
            if approve_request['device_status'] != 'Pending':
                return jsonify (
                    {
                        'status': 'FAILED',
                        'message': 'This request cannot be approved at the this time. It is not pending'
                    }
                )
            _request = database.modify_status(id, 'Approved')
            _id = _request['id']
            return jsonify(
                {
                    'status': 'OK',
                    'device-type': database.get_request(_id)['device_type'],
                    'fault-description': database.get_request(_id)['fault_description'],
                    'message': 'A request was modified',
                    'request-id': database.get_request(_id)['id'],
                    'device-status': database.get_request(_id)['device_status']
                }
            ), 200
        return jsonify (
                {
                    'status': 'FAILED',
                    'message': 'Access denied. Your do not have these rights.'
            }
            ), 400
    except:
        return jsonify (
                {
                    'status': 'FAILED',
                    'message': 'Invalid entry. Please check your request id.'
            }
            ), 400

#Admin disapprove a request
@app.route('/v1/requests/<id>/disapprove', methods = ['PUT'])
@token_required
def admin_disapprove_request(current_user, id):
    # Retrieve user
    user = database.get_user_byid(current_user['id'])
    # Test if admin
    if user['admin'] == True:
        if not database.get_request(id):
            return jsonify(
                {
                    'status': 'FAILED',
                    'message': 'Invalid request id. Id does not match any of your requests.'
                }
            ), 400
        _request = database.modify_status(id, 'Disapproved')
        _id = _request['id']
        return jsonify(
            {
                'status': 'OK',
                'device-type': database.get_request(_id)['device_type'],
                'fault-description': database.get_request(_id)['fault_description'],
                'message': 'A request was modified',
                'request-id': database.get_request(_id)['id'],
                'device-status': database.get_request(_id)['device_status']
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
    user = database.get_user_byid(current_user['id'])
    # Test if admin
    if user['admin'] == True:
        if not database.get_request(id):
            return jsonify(
                {
                    'status': 'FAILED',
                    'message': 'Invalid request id. Id does not match any of your requests.'
                }
            ), 400
        _request = database.modify_status(id, 'Resolved')
        _id = _request['id']
        return jsonify(
            {
                'status': 'OK',
                'device-type': database.get_request(_id)['device_type'],
                'fault-description': database.get_request(_id)['fault_description'],
                'message': 'A request was modified',
                'request-id': database.get_request(_id)['id'],
                'device-status': database.get_request(_id)['device_status']
            }
        ), 200
    return jsonify (
            {
                'status': 'FAILED',
                'message': 'Access denied. Your do not have these rights.'
        }
        ), 400