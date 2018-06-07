import uuid
import psycopg2

class DB():
    def __init__(self):
        self.conn = psycopg2.connect("dbname='username' user='username' password='Redfusion102' host='localhost' port='5432'")
        self.cur = self.conn.cursor()

    def add_user(self, username, password, admin = False):
        id = uuid.uuid1()
        self.cur.execute("INSERT INTO users VALUES('{}','{}','{}','{}')" .format(id, username, password, admin))
        self.conn.commit()

    def get_all_users(self):
        self.cur.execute("SELECT * from users")
        users = self.cur.fetchall()
        my_users = []
        for user in list(users):
            my_dict = {}
            my_dict['id'] = user[0]
            my_dict['username'] = user[1]
            my_dict['password'] = user[2]
            my_dict['admin'] = user[3]
            my_users.append(my_dict)
        return my_users

    def get_user_byid(self, id):
        self.cur.execute("SELECT * from users where id = '{}'" .format(id))
        user = self.cur.fetchone()
        my_dict = {}
        my_dict['id'] = user[0]
        my_dict['username'] = user[1]
        my_dict['password'] = user[2]
        my_dict['admin'] = user[3]
        return my_dict

    def get_user_byname(self, username):
        self.cur.execute("SELECT * from users where username = '{}'" .format(username))
        user = self.cur.fetchone()
        my_dict = {}
        my_dict['id'] = user[0]
        my_dict['username'] = user[1]
        my_dict['password'] = user[2]
        my_dict['admin'] = user[3]
        return my_dict

    def delete_user(self, item):
        self.cur.execute("DELETE FROM users where item='{}'" .format(item))
        self.conn.commit()

    def update_user(self, id, username, password, admin):
        self.cur.execute("UPDATE users SET username='{}', password='{}', admin='{}' where id='{}'" .format(username, password, admin, id))
        self.conn.commit()

    ###Request table methods

    def add_request(self, user_id, device_type, fault_description, device_status='Pending'):
        id = uuid.uuid1()
        self.cur.execute("INSERT INTO requests VALUES('{}','{}','{}','{}','{}')" .format(user_id, id, device_type, fault_description, device_status))
        self.conn.commit()
        return self.get_request(id)

    def get_all_requests(self):
        self.cur.execute("SELECT * from requests")
        requests = self.cur.fetchall()
        #return rows
        my_requests = []
        for request in requests:
            my_dict = {}
            my_dict['user_id'] = request[0]
            my_dict['id'] = request[1]
            my_dict['device_type'] = request[2]
            my_dict['fault_description'] = request[3]
            my_dict['device_status'] = request[4]
            my_requests.append(my_dict)
        return my_requests

    def get_user_requests(self, user_id):
        self.cur.execute("SELECT * FROM requests WHERE user_id = '{}'" .format(user_id))
        requests = self.cur.fetchall()
        my_requests = []
        for request in requests:
            my_dict = {}
            my_dict['user_id'] = request[0]
            my_dict['id'] = request[1]
            my_dict['device_type'] = request[2]
            my_dict['fault_description'] = request[3]
            my_dict['device_status'] = request[4]
            my_requests.append(my_dict)
        return my_requests

    def get_request(self, id):
        self.cur.execute("SELECT * FROM requests WHERE id = '{}'" .format(id))
        request = self.cur.fetchone()
        my_dict = {}
        my_dict['user_id'] = request[0]
        my_dict['id'] = request[1]
        my_dict['device_type'] = request[2]
        my_dict['fault_description'] = request[3]
        my_dict['device_status'] = request[4]
        return my_dict

    # def delete_request(self, item):
    #     self.cur.execute("DELETE FROM requests where item='{}'" .format(item))
    #     self.conn.commit()

    def modify_request(self, id, device_type, fault_description, device_status='Pending'):
        self.cur.execute("UPDATE requests SET device_type='{}', fault_description='{}', device_status='{}' where id='{}'" .format(device_type, fault_description, device_status, id))
        self.conn.commit()
        return self.get_request(id)

    def modify_status(self, id, device_status):
        self.cur.execute("UPDATE requests SET device_status='{}' where id='{}'" .format(device_status, id))
        self.conn.commit()
        return self.get_request(id)