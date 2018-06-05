import uuid

class User():
    def __init__(self):
        self.users = []
        id = uuid.uuid1()
        user = {'id':id, 'username': 'super', 'password': 'password', 'admin': True}
        self.users.append(user)

    def add_user(self, username, password, admin = False):
        id = uuid.uuid1()
        user = {'id':id, 'username': username, 'password': password}
        self.users.append(user)

    def get_user_byname(self, name):
        for user in self.users:
            if user['username'] == name:
                return user

    def get_user_byid(self, id):
        for user in self.users:
            if user['id'] == id:
                return user

    def get_all_users(self):
        return self.users

    def number_of_users(self):
        length = len(self.users)
        return length

class Request():
    def __init__(self):
        self.requests = []

    def add_request(self, device_type, fault_description, device_status = 'Pending'):
        id = uuid.uuid1()
        request = {'id':id, 'device_type': device_type, 'fault_description': fault_description, 'device_status': device_status}
        self.requests.append(request)

    def get_request_byid(self, id):
        for request in self.requests:
            if request['id'] == id:
                return request

    def get_request(self, index):
        return self.requests[index]

    def get_all_requests(self):
        return self.requests

    def modify_request(self, id, device_type, fault_description, device_status = 'Pending'):
        request = {'id':id, 'device_type': device_type, 'fault_description': fault_description, 'device_status': device_status}
        counter = 0
        for user in self.requests:
            if user['id'] == id:
                break
            counter += 1
        self.requests[counter] = request

    def number_of_requests(self):
        length = len(self.requests)
        return length