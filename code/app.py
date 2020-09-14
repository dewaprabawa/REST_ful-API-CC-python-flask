from flask import Flask
from flask_restful import Api, reqparse
from flask_jwt import JWT, jwt_required
from .security import authenticate, identity, UserRegister
from .item import Item,ItemList



app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret'
api = Api(app)

jwt = JWT(app,authenticate, identity)

api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList,"/items")
api.add_resource(UserRegister,"/register")


app.run(port=5000,debug=True)


