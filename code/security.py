from werkzeug.security import safe_str_cmp

class User(object):
    def __init__(self,_id, username, password):
        self._id = id
        self.username = username
        self.password = password
    
    def __str__(self):
        return "User(id='%s')" % self._id

users = [
    User(1,'bob','asdf')
]

username_mapping = {u.username:u for u in users}
userid_mapping = {u._id:u for u in users}


def authenticate(username, password):
    user = userid_mapping.get(username,None)
    if user and safe_str_cmp(user.password('utf-8'),password.encode('utf-8')):
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)