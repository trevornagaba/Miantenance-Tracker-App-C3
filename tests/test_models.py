from flask_testing import TestCase
from run import app
import json
from myapp.models import DB

class MyTests(TestCase):
    
    def create_app(self):
        return app

    # Test for successful user signup
    def test_add_user(self):
      