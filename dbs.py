

from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from datetime import datetime
from models import User


url = "mongodb://Ajay:root@cluster0-shard-00-00.uxwf7.mongodb.net:27017,cluster0-shard-00-01.uxwf7.mongodb.net:27017,cluster0-shard-00-02.uxwf7.mongodb.net:27017/ChatDb?ssl=true&replicaSet=atlas-47sly1-shard-0&authSource=admin&retryWrites=true&w=majority"
client = MongoClient(url)

db = client['ChatDb']
collection = db['users']

room_collection = db['rooms']
room_members_collection = db['room_members']



def save_user(username , email , password):
    password_hash = generate_password_hash(password)
    collection.insert_one({"_id":username , "email":email , "password":password_hash})

#save_user("Ajay" , "magarajay538@gmail.com" , "123456")

def get_user(username):
    data_user = collection.find_one({"_id":username})
    return User( data_user['_id'] ,data_user['email'] , data_user['password']) 


