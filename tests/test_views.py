from flask_testing import TestCase
from run import app
import json


class MyTests(TestCase):

    def create_app(self):
        self.admin_login_data = (
            {
                'username': 'Admin',
                'password': 'password',
            }
        )
        self.login_data = (
            {
                'username': 'loyce',
                'password': 'password',
            }
        )
        self.signup_data = (
            {
                'username': 'bebeto',
                'password': 'password',
                'reenter_password': 'not password'
            }
        )
        self.post_data = (
            {
                "device_type": "Laptop",
                "fault_description": "Battery malfunctioning"
            }
        )
        self.modify_data = (
            {
                "device_type": "computer",
                "fault_description": "Dead screen"
            }
        )
        return app

    # Test the view all requests endpoint
    def test_view_requests(self):
        with self.client:
            response = self.client.post(
                '/v1/auth/login',
                content_type='application/json',
                data=json.dumps(self.login_data)
            )
            reply = json.loads(response.data.decode())
            token = reply['token']
            response_2 = self.client.get(
                '/v1/users/requests',
                headers={'x-access-token': token}
            )
            reply_2 = json.loads(response_2.data.decode())
            self.assertEquals(reply_2['message'], 'successful')
            self.assertEquals(response_2.status_code, 200)

    # Test the view particular request endpoint
    def test_view_user_request(self):
        with self.client:
            # Login
            response = self.client.post(
                '/v1/auth/login',
                content_type='application/json',
                data=json.dumps(self.login_data)
            )
            reply = json.loads(response.data.decode())
            token = reply['token']
            response_2 = self.client.get(
                '/v1/users/requests/b57fc28f-6a5a-11e8-b0d5-a8a795b59b66',
                headers={'x-access-token': token}
            )
            reply_2 = json.loads(response_2.data.decode())
            self.assertTrue(
                reply_2['device-status'] in ['Pending', 'Disapproved', 'Approved', 'Resolved'], True)
            self.assertEquals(reply_2['message'], 'successful')
            self.assertTrue(response_2.status_code, 200)

    # Test the view particular request endpoint with someone else's request
    def test_view_user_request_fail(self):
        with self.client:
            # Login
            response = self.client.post(
                '/v1/auth/login',
                content_type='application/json',
                data=json.dumps(self.login_data)
            )
            reply = json.loads(response.data.decode())
            token = reply['token']
            response_2 = self.client.get(
                '/v1/users/requests/66b1188f-6a45-11e8-86dc-caca35d9aa6d',
                headers={'x-access-token': token}
            )
            reply_2 = json.loads(response_2.data.decode())
            self.assertEquals(reply_2['message'], 'You do not have access to this request.')
            self.assertTrue(response_2.status_code, 200)

    # Test the create a request endpoint with white space input
    def test_create_requests_fail(self):
        with self.client:
            self.post_data['device_type'] = '   '
            # Login
            response = self.client.post(
                '/v1/auth/login',
                content_type='application/json',
                data=json.dumps(self.login_data)
            )
            reply = json.loads(response.data.decode())
            token = reply['token']
            response_2 = self.client.post(
                '/v1/users/requests',
                content_type='application/json',
                data=json.dumps(self.post_data),
                headers={'x-access-token': token}
            )
            reply_2 = json.loads(response_2.data.decode())
            self.assertEquals(
                reply_2['message'], 'One of the required fields is empty')
            self.assertEquals(response_2.status_code, 400)
            
    # Test the modify a request endpoint with special characters input
    def test_modify_request_fail(self):
        with self.client:
            self.modify_data['username'] = '@#$$%^^'
            # Login
            response = self.client.post(
                '/v1/auth/login',
                content_type='application/json',
                data=json.dumps(self.login_data)
            )
            reply = json.loads(response.data.decode())
            token = reply['token']
            response_2 = self.client.put(
                '/v1/users/requests/034044cf-6a58-11e8-b842-a8a795b59b66',
                content_type='application/json',
                data=json.dumps(self.modify_data),
                headers={'x-access-token': token}
            )
            reply_2 = json.loads(response_2.data.decode())
            self.assertEquals(reply_2['message'],
                              'Invalid input. Check for symbols')
            self.assertEquals(response_2.status_code, 400)

    # Test the admin approve a request endpoint for failure
    def test_admin_approve_request(self):
        with self.client:
            # Login
            response = self.client.post(
                '/v1/auth/login',
                content_type='application/json',
                data=json.dumps(self.admin_login_data)
            )
            reply = json.loads(response.data.decode())
            token = reply['token']
            response_2 = self.client.put(
                '/v1/requests/034044cf-6a58-11e8-b842-a8a795b59b66/approve',
                content_type='application/json',
                data=json.dumps(self.modify_data),
                headers={'x-access-token': token}
            )
            reply_2 = json.loads(response_2.data.decode())
            self.assertEquals(
                reply_2['message'], 'This request cannot be approved at the this time. It is not pending')
            self.assertEquals(response_2.status_code, 200)

    # Test the admin disapprove a request endpoint
    def test_admin_dissapprove_request(self):
        with self.client:
            # Login
            response = self.client.post(
                '/v1/auth/login',
                content_type='application/json',
                data=json.dumps(self.admin_login_data)
            )
            reply = json.loads(response.data.decode())
            token = reply['token']
            response_2 = self.client.put(
                '/v1/requests/034044cf-6a58-11e8-b842-a8a795b59b66/disapprove',
                content_type='application/json',
                data=json.dumps(self.modify_data),
                headers={'x-access-token': token}
            )
            reply_2 = json.loads(response_2.data.decode())
            self.assertEquals(reply_2['device-status'], 'Disapproved')
            self.assertEquals(reply_2['device-type'],
                              self.modify_data['device_type'])
            self.assertEquals(response_2.status_code, 200)

    # Test the admin disapprove a request endpoint with invalid id
    def test_admin_dissapprove_request_fail(self):
        with self.client:
            # Login
            response = self.client.post(
                '/v1/auth/login',
                content_type='application/json',
                data=json.dumps(self.admin_login_data)
            )
            reply = json.loads(response.data.decode())
            token = reply['token']
            response_2 = self.client.put(
                '/v1/requests/034044cf-6a58-11e8-b842-a8a795/disapprove',
                content_type='application/json',
                data=json.dumps(self.modify_data),
                headers={'x-access-token': token}
            )
            reply_2 = json.loads(response_2.data.decode())
            self.assertEquals(reply_2['message'], 'Invalid request id. Id does not match any of the requests.')
            self.assertEquals(response_2.status_code, 400)

    # Test the admin resolve a request endpoint
    def test_admin_resolve_request(self):
        with self.client:
            # Login
            response = self.client.post(
                '/v1/auth/login',
                content_type='application/json',
                data=json.dumps(self.admin_login_data)
            )
            reply = json.loads(response.data.decode())
            token = reply['token']
            response_2 = self.client.put(
                '/v1/requests/034044cf-6a58-11e8-b842-a8a795b59b66/resolve',
                content_type='application/json',
                data=json.dumps(self.modify_data),
                headers={'x-access-token': token}
            )
            reply_2 = json.loads(response_2.data.decode())
            self.assertEquals(reply_2['device-status'], 'Resolved')
            self.assertEquals(reply_2['device-type'],
                              self.modify_data['device_type'])
            self.assertEquals(response_2.status_code, 200)

    # Test the admin view all requests endpoint
    def test_admin_view_request(self):
        with self.client:
            # Login
            response = self.client.post(
                '/v1/auth/login',
                content_type='application/json',
                data=json.dumps(self.admin_login_data)
            )
            reply = json.loads(response.data.decode())
            token = reply['token']
            response_2 = self.client.get(
                '/v1/requests',
                data=json.dumps(self.modify_data),
                headers={'x-access-token': token}
            )
            reply_2 = json.loads(response_2.data.decode())
            self.assertEquals(reply_2['message'], 'successful')
            self.assertEquals(response_2.status_code, 200)

    # Test the admin view all requests endpoint with none admin login
    def test_admin_view_request_fail(self):
        with self.client:
            # Login
            response = self.client.post(
                '/v1/auth/login',
                content_type='application/json',
                data=json.dumps(self.login_data)
            )
            reply = json.loads(response.data.decode())
            token = reply['token']
            response_2 = self.client.get(
                '/v1/requests',
                data=json.dumps(self.modify_data),
                headers={'x-access-token': token}
            )
            reply_2 = json.loads(response_2.data.decode())
            self.assertEquals(reply_2['message'], 'You do not have these permissions')
            self.assertEquals(response_2.status_code, 400)
