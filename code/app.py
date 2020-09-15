from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from .security import authenticate, identity, UserRegister
from .item import Item,ItemList

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret'
app.secret_key = "ddqq"
api = Api(app)

jwt = JWT(app,authenticate, identity) #/auth

api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList,"/items")
api.add_resource(UserRegister,"/register")

if __name__ == "__main__":
    app.run(port=5000,debug=True)


