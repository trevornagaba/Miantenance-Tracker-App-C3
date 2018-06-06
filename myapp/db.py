import psycopg2

class DB():
    def __init__(self):
        self.conn = psycopg2.connect("dbname='username' user='username' password='Redfusion102' host='localhost' port='5432'")
        self.cur = self.conn.cursor()

    def insert_user(self, id, username, password, admin):
        self.cur.execute("CREATE TABLE IF NOT EXISTS users (id TEXT, username TEXT, password TEXT, admin BOOL)")
        self.cur.execute("INSERT INTO users VALUES('{}','{}','{}','{}')" .format(id, username, password, admin))
        self.conn.commit()

    def view_all_users(self):
        self.cur.execute("SELECT * from users")
        rows = self.cur.fetchall()
        return list(rows)

    def view_user(self, id):
        self.cur.execute("SELECT * from users where id = '{}'" .format(id))
        user = self.cur.fetchone()
        return user

    def view_user_byname(self, username):
        self.cur.execute("SELECT * from users where username = '{}'" .format(username))
        user = self.cur.fetchone()
        return user

    def delete_user(self, item):
        self.cur.execute("DELETE FROM users where item='{}'" .format(item))
        self.conn.commit()

    def update_user(self, id, username, password, admin):
        self.cur.execute("UPDATE users SET username='{}', password='{}', admin='{}' where id='{}'" .format(username, password, admin, id))
        self.conn.commit()

    ###Request table methods

    def insert_request(self, user_id, id, device_type, fault_description, device_status):
        self.cur.execute("CREATE TABLE IF NOT EXISTS requests (user_id TEXT, id TEXT, device_type TEXT, fault_description TEXT, device_status TEXT)")
        self.cur.execute("INSERT INTO requests VALUES('{}','{}','{}','{}','{}')" .format(user_id, id, device_type, fault_description, device_status))
        self.conn.commit()

    def view_all_requests(self):
        self.cur.execute("SELECT * from requests")
        rows = self.cur.fetchall()
        return rows

    def view_user_requests(self, user_id):
        self.cur.execute("SELECT * FROM requests WHERE user_id = '{}'" .format(user_id))
        request = self.cur.fetchall()
        return request

    def view_one_request(self, id):
        self.cur.execute("SELECT * FROM requests WHERE id = '{}'" .format(id))
        request = self.cur.fetchone()
        return request

    def delete_request(self, item):
        self.cur.execute("DELETE FROM requests where item='{}'" .format(item))
        self.conn.commit()

    def update_request(self, device_type, fault_description, device_status, id):
        self.cur.execute("UPDATE requests SET device_type='{}', fault_description='{}', device_status='{}' where id='{}'" .format(device_type, fault_description, device_status, id))
        self.conn.commit()

    def update_status(self, device_status, id):
        self.cur.execute("UPDATE requests SET device_status='{}' where id='{}'" .format(device_status, id))
        self.conn.commit()