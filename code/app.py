from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required, current_identity
from security import authenticate, identity, UserRegister



app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret'
api = Api(app)

jwt = JWT(app,authenticate, identity)

items = []

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price",type=float, required=True, help="This field can not be left blank!")
    
    @jwt_required
    def get(self, name):
        item = next(filter(lambda x:x["name"] == name, items), None)
        return {"item":item}, 200 if item else 404 #200 if item is not None else 404
    
    def post(self,name):
        if next(filter(lambda x:x["name"] == name,items),None):
            return {"message":"An item with name '{}' already existed".format(name)},400
        
        data = Item.parser.parse_args()    
        item = {"name":name, "price":data["price"]}
        items.append(item)
        return item, 201
    
    def delete(self,name):
        global items
        items = list(filter(lambda x:x["name"] != name,items))
        return {"items":"item named '{}' has deleted".format(name)}

    def put(self,name):
        data = Item.parser.parse_args()
        item = next(filter(lambda x:x["name"] == name, items), None)
        if item is None:
            item = {"name":name, "price":data['price']}
            items.append(item)
        else:
            item.update(data)
        return item

class ItemList(Resource):
    def get(self):
        return {"items":items}


@app.route('/protected')
@jwt_required()
def protected():
    return '%s' % current_identity

api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList,"/items")
api.add_resource(UserRegister,"/register")


app.run(port=5000,debug=True)


