from flask_testing import TestCase
from myapp import app
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
                'username': 'Jack',
                'password': 'password',
                'reenter_password': 'password'
            }
        )
        return app

    # Test signup with taken username
    def test_signup_successful(self):
        with self.client:
            response = self.client.post(
                '/v1/auth/signup',
                content_type='application/json',
                data=json.dumps(self.signup_data)
            )
            reply = response.data
            self.assertEquals(reply, 'Invalid username')
            self.assertEquals(response.status_code, 200)

    # Test for signup with wrong reenter_password
    def test_signup_fail(self):
        with self.client:
            self.signup_data['password'] = 'wrong password'
            response = self.client.post(
                '/v1/auth/signup',
                content_type='application/json',
                data=json.dumps(self.signup_data)
            )
            reply = response.data
            self.assertEquals(reply['message'], 'Your passwords do not match')
            self.assertEquals(response.status_code, 400)

    # Test for signup with wrong reenter_password
    def test_signup_fail_special_characters(self):
        with self.client:
            self.signup_data['username'] = '@#$%#'
            response = self.client.post(
                '/v1/auth/signup',
                content_type='application/json',
                data=json.dumps(self.signup_data)
            )
            reply = response.data
            self.assertEquals(reply['message'],
                              'Invalid input. Check for symbols')
            self.assertEquals(response.status_code, 400)

    # Test for successful user login
    def test_login_successful(self):
        with self.client:
            response = self.client.post(
                '/v1/auth/login',
                content_type='application/json',
                data=json.dumps(self.login_data),
            )
            reply = response.data
            self.assertEquals(
                reply['user']['username'], self.login_data['username'])
            self.assertEquals(response.status_code, 201)

    # Test for login with wrong password

    def test_login_fail(self):
        with self.client:
            self.login_data['password'] = 'wrong pasword'
            response = self.client.post(
                '/v1/auth/login',
                content_type='application/json',
                data=json.dumps(self.login_data)
            )
            reply = response.data
            self.assertEquals(
                reply['message'],
                'Could not verify. Please check your login details')
            self.assertEquals(response.status_code, 400)

    # Test for loginup with unknown user
    def test_login_fail_special_characters(self):
        with self.client:
            self.login_data['username'] = 'no_user'
            response = self.client.post(
                '/v1/auth/login',
                content_type='application/json',
                data=json.dumps(self.login_data)
            )
            reply = response.data
            self.assertEquals(reply['message'],
                              'Could not verify. No user found.')
            self.assertEquals(response.status_code, 400)

        # Test for loginup with missing field
    def test_login_fail_missinf_field(self):
        with self.client:
            self.login_data['username'] = ''
            response = self.client.post(
                '/v1/auth/login',
                content_type='application/json',
                data=json.dumps(self.login_data)
            )
            reply = response.data
            self.assertEquals(reply['message'],
                              'One of your login fields is missing.')
            self.assertEquals(response.status_code, 400)