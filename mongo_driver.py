from pymongo import MongoClient
from pymongo import collection
import os
from dotenv import load_dotenv
from torn_client import User as TornUser

load_dotenv()
def get_database():
    CONNECTION_URL = os.environ["MONGO_CONNECTION_URL"]
    client = MongoClient(CONNECTION_URL)
    return client["user_data"]

def user_to_db(user_id: str, torn_user: TornUser) -> dict: 
    """Utility function to take a user and its id and format it for the database
    
    :Parameters:
        -`user_id`: the discord id of the user
        -`torn_user`: the TornUser object corresponding to that id"""
    
    res = {
        "_id": user_id, 
        "user_data" : torn_user.as_mongodoc() 
    }
    return res

def alreadyExists(newID: str, collection: collection):
    return collection.count_documents({"_id": newID},limit = 1) != 0

    

if __name__ == "__main__":
    db = get_database()
    users_collection= db["users"]
    user1 = {
        "_id" :235894085922193408,
        "key": "L1ZLIuYKllusUNts",
        "item_dict" : {"1": 1_000_000} 
    }
    torn_user = TornUser("L1ZLIuYKllusUNts")
    torn_user.add_item(1, 1_0000_000)
    user2 = user_to_db(235894085922193407, torn_user)
    if alreadyExists(user2["_id"], users_collection):
        print(user2["_id"], " already exists")
    else:
        users_collection.insert_one(user2)
    items = users_collection.find()
    print(type(items))
    for item in items:
        print(item, type(item))
