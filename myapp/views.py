from flask import Blueprint
from myapp.api import UserRequests, AdminRequests
from myapp.auth import Auth

user_requests = Blueprint('user_requests', __name__)
admin_requests = Blueprint('admin_requests', __name__)
auth_requests = Blueprint('auth_requests', __name__)


user_requests_view = UserRequests.as_view('user_requests')

admin_requests_view = AdminRequests.as_view('admin_requests')

auth_requests_view = Auth.as_view('auth_requests')


user_requests.add_url_rule('/v1/users/requests',
                           view_func=user_requests_view, methods=['GET', 'POST'])

user_requests.add_url_rule('/v1/users/requests/<id>',
                           view_func=user_requests_view, methods=['GET', 'PUT'])

admin_requests.add_url_rule('/v1/requests',
                            view_func=admin_requests_view, methods=['GET'])

admin_requests.add_url_rule('/v1/requests/<id>/<action>',
                            view_func=admin_requests_view, methods=['PUT'])

auth_requests.add_url_rule('/v1/auth/<action>',
                           view_func=auth_requests_view, methods=['POST'])