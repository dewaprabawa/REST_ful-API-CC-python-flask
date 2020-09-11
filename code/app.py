from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT
from .security import authenticate, identity

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret'
api = Api(app, authenticate, identity)

jwt = JWT(app,)

items = []

class Item(Resource):
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


api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList,"/items")

app.run(port=5000)