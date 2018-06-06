import uuid
from myapp.db import DB

database = DB()

class User():
    def __init__(self):
        self.users = []
        id = uuid.uuid1()
        user = {'id':id, 'username': 'super', 'password': 'password', 'admin': True}
        self.users.append(user)

    def add_user(self, username, password, admin = False):
        id = uuid.uuid1()
        user = {'id':str(id), 'username': username, 'password': password, 'admin': admin}
        # self.users.append(user)
        database.insert_user(user['id'], user['username'], user['password'], user['admin'])

#Update to use id through token
    def get_user_byname(self, name):
        user = database.view_user_byname(name)
        userz = {}
        userz['id'] = user[0]
        userz['username'] = user[1]
        userz['password'] = user[2]
        userz['admin'] = user[3]
        return userz

    def get_user_byid(self, id):
        user = database.view_user(id)
        userz = {}
        userz['id'] = user[0]
        userz['username'] = user[1]
        userz['password'] = user[2]
        userz['admin'] = user[3]
        return userz

    def get_all_users(self):
        my_users = []
        for userz in database.view_all_users():
            my_dict = {}
            my_dict['id'] = userz[0]
            my_dict['username'] = userz[1]
            my_dict['password'] = userz[2]
            my_dict['admin'] = userz[3]
            my_users.append(my_dict)
        return my_users

    def number_of_users(self):
        length = len(self.users)
        return length

class Request():
    def __init__(self):
        self.requests = []

    def add_request(self, user_id, device_type, fault_description, device_status = 'Pending'):
        id = uuid.uuid1()
        request = {'user_id': user_id, 'id':id, 'device_type': device_type, 'fault_description': fault_description, 'device_status': device_status}
        database.insert_request(request['user_id'], request['id'], request['device_type'], request['fault_description'], request['device_status'])
        return database.view_one_request(request['id'])

    def get_request(self, id):
        my_request = database.view_one_request(id)
        my_dict = {}
        my_dict['user_id'] = my_request[0]
        my_dict['id'] = my_request[1]
        my_dict['device_type'] = my_request[2]
        my_dict['fault_description'] = my_request[3]
        my_dict['device_status'] = my_request[4]
        return my_dict

    def get_user_requests(self, user_id):
        my_requests = []
        for requestz in database.view_user_requests(user_id):
            my_dict = {}
            my_dict['user_id'] = requestz[0]
            my_dict['id'] = requestz[1]
            my_dict['device_type'] = requestz[2]
            my_dict['fault_description'] = requestz[3]
            my_dict['device_status'] = requestz[4]
            my_requests.append(my_dict)
        return my_requests

    def get_all_requests(self):
        my_requests = []
        for requestz in database.view_all_requests():
            my_dict = {}
            my_dict['user_id'] = requestz[0]
            my_dict['id'] = requestz[1]
            my_dict['device_type'] = requestz[2]
            my_dict['fault_description'] = requestz[3]
            my_dict['device_status'] = requestz[4]
            my_requests.append(my_dict)
        return my_requests

    def modify_request(self, id, device_type, fault_description, device_status = 'Pending'):
        request = {'id':id, 'device_type': device_type, 'fault_description': fault_description, 'device_status': device_status}
        database.update_request(request['device_type'], request['fault_description'], request['device_status'], request['id'])
        return database.view_one_request(request['id'])

    def number_of_requests(self):
        length = len(self.requests)
        return length