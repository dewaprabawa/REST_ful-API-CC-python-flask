from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price",type=float, required=True, help="This field can not be left blank!")
    
    @jwt_required
    def get(self, name):
        item = self.find_by_name(name)
        if item: 
            return item
        return {"message":"item not found"},404
    
    @classmethod
    def find_by_name(cls,name):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query,(name,))
        row = result.fetchone()
        connection.close()
        if row:
            return {"item":{"name":row[0],"price":row[1]}}
        
    
    def post(self,name):
        if self.find_by_name(name):
            return {"message":"An item with name '{}' already existed".format(name)},400
        
        data = Item.parser.parse_args()    
        item = {"name":name, "price":data["price"]}
        
        try:
            self.insertItem(item)
        except:
            return {"message":"An error occurred when inserting Item."},500 # error occured internally
        return item, 201
    
    @classmethod
    def insertItem(cls,item):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        
        query = "INSERT INTO items VALUES (?,?)"
        cursor.execute(query,(item["name"],item["price"]))
        
        connection.commit()
        connection.close()
    
    def delete(self,name):
        #global items
        #items = list(filter(lambda x:x["name"] != name,items))
        
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        
        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query,(name,))
        
        connection.commit()
        connection.close()
        
        return {"items":"item named '{}' has deleted".format(name)}
       
       
    def put(self,name):
        data = Item.parser.parse_args()
        item = self.find_by_name(name)
        update_item = {"name":name, "price":data["price"]}
        
        if item is None:
            try:
                self.insertItem(update_item)
            except: 
                return {"message": "An error occurred inserting the item"},500
        else:
            try:
                self.update(update_item)
            except:
                return {"message": "An error occurred updating the item"},500 
        return update_item
    
    
    @classmethod
    def update(cls,item):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        
        query = "UPDATE items price=? WHERE name=?"
        cursor.execute(query,(item["price"],item["name"]))
        
        connection.commit()
        connection.close()
        

class ItemList(Resource):
    def get(self):
        return {"items":items}

