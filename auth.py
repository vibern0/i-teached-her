import redis
import sqlite3
import os, hashlib

# global vars
redis_connection = None
sqlite_database_name = 'example.db'

def connect_to_redis():
    try:
        global redis_connection
        redis_connection = redis.StrictRedis()
        redis_connection.ping()
        print("connected to redis!")
    except Exception:
        exit('Failed to connect, terminating.')


def auth_from_sqlite(username, password):
    with sqlite3.connect(sqlite_database_name) as sqlite_connection:
        c = sqlite_connection.cursor()
        c.execute('SELECT pass FROM users where username=?', (username,))
        if c.fetchone()[0] == password:
            # thanks to https://stackoverflow.com/a/44273556/3348623
            token = hashlib.md5(os.urandom(32)).hexdigest()
            redis_connection.set(token, username, 60)
            return token
        else:
            return ''


def get_username_by_token(token):
    return redis_connection.get(token)


def validate_user_permissions(username):
    return (username == b'miriam') # just for example


def request_info(info_requested):
    with sqlite3.connect(sqlite_database_name) as sqlite_connection:
        c = sqlite_connection.cursor()
        c.execute('SELECT v FROM server_info where k = ?', (info_requested,))
        return c.fetchone()[0]