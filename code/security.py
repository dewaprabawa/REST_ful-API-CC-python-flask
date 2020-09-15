from werkzeug.security import safe_str_cmp
import sqlite3
from flask_restful import Resource, reqparse

class User(object):
    TABLE_NAME = 'users'
    
    def __init__(self,_id, username, password):
        self._id = id
        self.username = username
        self.password = password
        
    @classmethod   
    def find_by_username(cls,username):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        
        query = "SELECT * FROM users WHERE username=?".format(table=cls.TABLE_NAME)
        result = cursor.execute(query,(username,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else: user = None
        
        connection.close()
        return user
        
    @classmethod
    def find_by_id(cls,_id):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        
        query = "SELECT * FROM users WHERE id=?".format(table=cls.TABLE_NAME)
        result = cursor.execute(query,(_id,))
        row = result.fetchone()
        
        if row:
            user = cls(*row)
        else: user = None
        connection.close()
        return user
        
    
    def __str__(self):
        return "User(id='%s')" % self._id

class UserRegister(Resource):
    TABLE_NAME = "users"
    
    parser = reqparse.RequestParser()
    parser.add_argument("username",type=str,required=True,help="This field cannot be left blank!")
    parser.add_argument("password",type=str,required=True,help="This field cannot be left blank!")
    
    def post(self):
        data = UserRegister.parser.parse_args()
        if User.find_by_username(data["username"]):
            return {"message":"User with that username already exist"},400
        
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        query = "INSERT INTO {table} VALUES (NUll,?,?)".format(table = self.TABLE_NAME)
        cursor.execute(query, (data['username'], data['password']))
        
        connection.commit()
        connection.close()
        
        return {"message":"User created successfully"}, 201
        

def authenticate(username, password):
    user = User.find_by_username(username)
    if user and safe_str_cmp(user.password('utf-8'),password.encode('utf-8')):
        return user

def identity(payload):
    user_id = payload['identity']
    return User.find_by_id(user_id)

