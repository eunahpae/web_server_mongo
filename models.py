from pymongo import MongoClient
import datetime
from passlib.hash import pbkdf2_sha256
from bson.objectid import ObjectId
from config import MONGODB_URL


def hash_password(original_passwod):
    salt = 'eungok'
    password = original_passwod + salt
    password = pbkdf2_sha256.hash(password)
    return password
    
def check_password(input_password, hashed_password):
    salt = 'eungok'
    password=input_password + salt
    result=pbkdf2_sha256.verify(password, hashed_password)   
    return result   
    
class MyMongo:
    def __init__(self, db_url, database):
        self.db_url = db_url
        self.database = database
        self.client = MongoClient(db_url)
        self.db = self.client.database
        
    def user_insert(self, username, email,phone,password):
        db = self.client.os
        users = db.users
        pw = hash_password(password)
        user = {
            "username":username,
            "email":email,
            "phone":phone,
            "password":pw,
            "create_at":datetime.datetime.utcnow()
        }
        result = users.insert_one(user)
        print(result)
        return 1
        
    def verify_password(self,input_password, id): 
        db = self.client.os
        users = db.users      
        user = users.find_one({'_id':id}) 
        if user:
            result = check_password(input_password,user['password'])
            if result:
                print('Verify Success')
            else:
                print("Verify Fail")
        else:
            print("ID is not founded.")        
    

mymango = MyMongo(MONGODB_URL, 'os')
mymango.verify_password("1234", ObjectId('64ba26436b5bac3f54684a45'))    
        

# mongodb_URI = MONGODB_URL
# client = MongoClient(mongodb_URI)
# print(client.list_database_names())

# db = client.os
# users = db.users

# hashed_pw = hash_password("1234")
# print(hashed_pw)


# # result = users.insert_one(user)
# # print(result)

# user=users.find_one({"_id": ObjectId('64ba26436b5bac3f54684a45')})
# # print(user)

# result = check_password("1234", user['password'])
# print(result)