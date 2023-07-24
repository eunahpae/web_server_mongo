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
        
    def verify_password(self, email, input_password): 
        db = self.client.os
        users = db.users      
        user = users.find_one({'email':email}) 
        # print(user)
        if user:
            result = check_password(input_password,user['password'])
            if result:
                print('Verify Success')
                return "1"
            else:
                print("Verify Fail")
                return "2"
        else:
            print("ID is not founded.")
            return "3"
            
    def find_user(self, email):
        db = self.client.os
        users = db.users      
        user = users.find_one({'email':email}) 
        # print(user)
        return user
    
    def find_data(self):
        db = self.client.os
        lists = db.lists      
        list = lists.find()
        # for i in list:
        #     print(i)
        return list
    
    def insert_data(self, title, desc, author):
        db = self.client.os
        lists = db.lists
        data = {
            'title':title,
            'desc':desc,
            'author':author,
            'create_at':datetime.datetime.utcnow()
        }      
        list = lists.insert_one(data)
        # for i in list:
        #     print(i)
        return list
    
    def edit_data(self, title, desc, author):
        db = self.client.os
        lists = db.lists
        data = {
            'title':title,
            'desc':desc,
            'author':author,
            'create_at':datetime.datetime.utcnow()
        }      
        list = lists.insert_one(data)
        # for i in list:
        #     print(i)
        return list
    
    def delete_data(self, title):
        db = self.client.os
        lists = db.lists
        data = self.find_data(title)    
        delete = lists.deleteOne(data)
        # for i in list:
        #     print(i)             
    

# mymongo = MyMongo(MONGODB_URL, 'os')
# # mymongo.verify_password('1@naver.com','1234')    
# # mymongo.find_user('1@naver.com','1234')
# mymongo.find_data()

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