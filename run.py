from myapp import app
from myapp import views
from myapp import api
from myapp import auth
from myapp.views import user_requests, admin_requests, auth_requests


if __name__ == '__main__':
    app.register_blueprint(user_requests)
    app.register_blueprint(admin_requests)
    app.register_blueprint(auth_requests)
    app.run(debug='True')
