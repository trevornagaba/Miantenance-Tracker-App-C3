import psycopg2
import uuid
from werkzeug.security import generate_password_hash

id = uuid.uuid1()
admin_password = generate_password_hash('password', method='sha256')

# Create users table, requests table and admin
def create_tables():
    conn = psycopg2.connect("dbname='username' user='username' password='Redfusion102' host='localhost' port='5432'")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (id TEXT, username TEXT, password TEXT, admin BOOL)")
    cur.execute("CREATE TABLE IF NOT EXISTS requests (user_id TEXT, id TEXT, device_type TEXT, fault_description TEXT, device_status TEXT)")
    cur.execute("INSERT INTO users VALUES('{}','{}','{}','{}')" .format(id, 'Admin', admin_password, True))
    conn.commit()
    conn.close()
        
create_tables()