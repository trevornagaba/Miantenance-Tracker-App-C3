from flask import Flask, request, jsonify
import json
from myapp import app
from myapp.models import DB
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
from myapp.auth import Auth

app.config['SECRET KEY'] = 'thisissecret'

database = DB()
auth = Auth()


@app.route('/v1/users/requests', methods=['POST'])
@auth.token_required
def create_requests(current_user):
    # Retrieve the data
    data = request.get_json()
    # Validate the data
    if data['device_type'] == "" or data['fault_description'] == "":
        return jsonify(
            {
                'status': 'FAILED',
                'message': 'One of the required fields is empty'
            }
        ), 400
    try:
        if isinstance(data['device_type'].encode(), str) and isinstance(data['fault_description'].encode(), str):
            # Create id and store the data
            _request = database.add_request(
                current_user['id'], data['device_type'], data['fault_description'])
            id = _request['id']
            return jsonify(
                {
                    'status': 'OK',
                    'message': 'Request created successfully',
                    'device-status': database.get_request(id)['device_status'],
                    'device-type': database.get_request(id)['device_type'],
                    'request-id': database.get_request(id)['id']
                }
            ), 201
    except AttributeError:
        return jsonify(
            {
                'status': 'FAILED',
                'message': 'Invalid request. Please check your entry',
            }
        ), 400

# Fetch all requests of a logged in user


@app.route('/v1/users/requests', methods=['GET'])
@auth.token_required
def view_requests(current_user):
    try:
        return jsonify(
            {
                'status': 'OK',
                'message': 'successful',
                'requests': database.get_user_requests(current_user['id'])
            }
        ), 200
    except:
        return jsonify(
            {
                'status': 'FAILED',
                'message': 'No requests added',
            }
        ), 404

# Fetch a request that belongs to a logged in user


@app.route('/v1/users/requests/<id>', methods=['GET'])
@auth.token_required
def view_user_requests(current_user, id):
    # Catch request for an id that does not exist in db
    try:
        # Test if correct user
        request = database.get_request(id)
        if request['user_id'] == current_user['id']:
            # Validate request
            return jsonify(
                {
                    'status': 'OK',
                    'message': 'successful',
                    'device-type': database.get_request(id)['device_type'],
                    'fault description': database.get_request(id)['fault_description'],
                    'device-status': database.get_request(id)['device_status'],
                    'id': database.get_request(id)['id']
                }
            ), 200
        return jsonify(
            {
                'status': 'FAILED',
                'message': 'You do not have access to this request.'
            }
        ), 404
    except:
        return jsonify(
            {
                'status': 'FAILED',
                'message': 'This request does not exist'
            }
        ), 404

# Modify a request


@app.route('/v1/users/requests/<id>', methods=['PUT'])
@auth.token_required
def modify_requests(current_user, id):
    # Test if status is approved
    try:
        modify_request = database.get_request(id)
        if modify_request['user_id'] != current_user['id']:
            return jsonify(
                {
                    'status': 'FAILED',
                    'message': 'Access denied. This request belongs to another user.'
                }
            ), 400
        if modify_request['device_status'] == 'Approved':
            return jsonify(
                {
                    'status': 'FAILED',
                    'message': 'This request cannot be modified at this time. It has already been approved.'
                }
            ), 400
    except:
        return jsonify(
            {
                'status': 'FAILED',
                'message': 'This request does not exist.'
            }
        ), 400
    # Retrieve the request
    data = request.get_json()
    # Validate the data
    if data['device_type'] == "" or data['fault_description'] == "":
        return jsonify(
            {
                'status': 'FAILED',
                'message': 'One of the required fields is empty'
            }
        ), 400
    try:
        if isinstance(data['device_type'].encode(), str) and isinstance(data['fault_description'].encode(), str):
            # Store the data
            _request = database.modify_request(
                id, data['device_type'], data['fault_description'])
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


# Admin fetch all requests of all users
@app.route('/v1/requests', methods=['GET'])
@auth.token_required
def admin_view_requests(current_user):
    # Test if admin
    user = database.get_user_byid(current_user['id'])
    # Add test for requests in db
    if user['admin'] == False:
        return jsonify(
            {
                'status': 'FAILED',
                'message': 'You do not have these permissions',
            }
        ), 400
    return jsonify(
        {
            'status': 'OK',
            'message': 'successful',
            'requests': database.get_all_requests()
        }
    ), 200


# Admin approve a request
@app.route('/v1/requests/<id>/approve', methods=['PUT'])
@auth.token_required
def admin_approve_request(current_user, id):
    try:
        # Retrieve user
        user = database.get_user_byid(current_user['id'])
        # Test if admin
        if user['admin'] == True:
            approve_request = database.get_request(id)
            if approve_request['device_status'] != 'Pending':
                return jsonify(
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
        return jsonify(
            {
                'status': 'FAILED',
                'message': 'Access denied. Your do not have these rights.'
            }
        ), 400
    except:
        return jsonify(
            {
                'status': 'FAILED',
                'message': 'Invalid entry. Please check your request id.'
            }
        ), 400


# Admin disapprove a request
@app.route('/v1/requests/<id>/disapprove', methods=['PUT'])
@auth.token_required
def admin_disapprove_request(current_user, id):
    # Retrieve user
    user = database.get_user_byid(current_user['id'])
    # Test if admin
    if user['admin'] == True:
        try:
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
        except:
            return jsonify(
                {
                    'status': 'FAILED',
                    'message': 'Invalid request id. Id does not match any of your requests.'
                }
            ), 400
    return jsonify(
        {
            'status': 'FAILED',
            'message': 'Access denied. Your do not have these rights.'
        }
    ), 400

# Admin resolve a request


@app.route('/v1/requests/<id>/resolve', methods=['PUT'])
@auth.token_required
def admin_resolve_request(current_user, id):
    # Retrieve user
    user = database.get_user_byid(current_user['id'])
    # Test if admin
    if user['admin'] == True:
        try:
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
        except:
            return jsonify(
                {
                    'status': 'FAILED',
                    'message': 'Invalid request id. Id does not match any of your requests.'
                }
            ), 400
    return jsonify(
        {
            'status': 'FAILED',
            'message': 'Access denied. Your do not have these rights.'
        }
    ), 400
