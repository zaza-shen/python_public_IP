from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def validate_register( user ):
        is_valid = True
        if len(user["first_name"])<2:
            flash(u"Your first name contains only one character or nothing.", "register")
            is_valid = False
        if len(user["last_name"])<2:
            flash(u"Your last name contains only one character or nothing.", "register")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash(u"Invalid email address!", "register")
            is_valid = False
        if not len(user["password"]):
            flash(u"Your password contains nothing.", "register")
            is_valid = False
        if user['c_password']!=user['password']:
            flash(u"Your confirmed password is different from your password.", "register")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_email( user_login ):
        is_valid = True
        data = {
            'email' : user_login['email'],
            'password' : user_login['password']
        }
        query = 'SELECT * FROM users WHERE email=%(email)s'
        results = connectToMySQL('tv_shows_schema').query_db(query, data)
        if not results:
            is_valid = False
            flash(u'Invalid email address!', 'login')
            return is_valid 
        # print('This is results', results) 
        return results[0]

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users"
        results = connectToMySQL('tv_shows_schema').query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users

    @classmethod
    def get_pwd_by_email(cls, i_email):
        data = {
            'email' : i_email
        }
        query = "SELECT * FROM users WHERE email=%(email)s"
        result = connectToMySQL('tv_shows_schema').query_db(query, data)
        if not result:
            return False
        return result[0]

    @classmethod
    def get_show_poster(cls, data):
        query = "SELECT first_name, last_name FROM shows LEFT JOIN users ON shows.user_id = users.id WHERE shows.id = %(id)s;"
        result = connectToMySQL('tv_shows_schema').query_db(query, data)
        if not result:
            return False
        return result[0]

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL('tv_shows_schema').query_db(query, data)
        # print("__________",data, query, results)
        if not results:
            return False
        return results[0]

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) values (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL("tv_shows_schema").query_db(query, data)

    @classmethod
    def unlike(cls, data):
        query = "DELETE FROM likes WHERE user_id = %(user_id)s AND show_id= %(show_id)s;"
        return connectToMySQL("tv_shows_schema").query_db(query, data)

    @classmethod
    def like(cls, data):
        query = "INSERT INTO likes (user_id, show_id) values  (%(user_id)s, %(show_id)s);"
        return connectToMySQL("tv_shows_schema").query_db(query, data)