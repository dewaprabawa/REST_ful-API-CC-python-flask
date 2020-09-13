from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp



app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret'
api = Api(app)

items = []

class Item(Resource):
    @jwt_required
    def get(self, name):
        item = next(filter(lambda x:x["name"] == name, items), None)
        return {"item":item}, 200 if item else 404 #200 if item is not None else 404
    
    def post(self,name):
        if next(filter(lambda x:x["name"] == name,items),None):
            return {"message":"An item with name '{}' already existed".format(name)},400
            
        data = request.get_json()
        item = {"name":name, "price":data["price"]}
        items.append(item)
        return item, 201


class ItemList(Resource):
    def get(self):
        return {"items":items}



class User(object):
    def __init__(self,_id, username, password):
        self._id = id
        self.username = username
        self.password = password
    
    def __str__(self):
        return "User(id='%s')" % self._id

users = [
    User(1,"bob","asdf")
]

username_mapping = {u.username:u for u in users}
userid_mapping = {u._id:u for u in users}

def authenticate(username, password):
    print(username_mapping)
    user = userid_mapping.get(username,None)
    if user and safe_str_cmp(user.password('utf-8'),password.encode('utf-8')):
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)


@app.route('/auth')
@jwt_required()
def auth():
    return '%s' % current_identity


jwt = JWT(app,authenticate, identity)

api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList,"/items")


app.run(port=5000,debug=True)


