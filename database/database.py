#Codeflix_Botz
#rohit_1888 on Tg

import motor, asyncio
import motor.motor_asyncio
from config import DB_URI, DB_NAME
import certifi
from pymongo import MongoClient
from config import DB_URI, DB_NAME

client = MongoClient(DB_URI)
db = client[DB_NAME]
batch_collection = db["batch_links"]

dbclient = motor.motor_asyncio.AsyncIOMotorClient(DB_URI, tlsCAFile=certifi.where())
database = dbclient[DB_NAME]

user_data = database['users']

default_verify = {
    'is_verified': False,
    'verified_time': 0,
    'verify_token': "",
    'link': ""
}

def new_user(id):
    return {
        '_id': id,
        'verify_status': {
            'is_verified': False,
            'verified_time': "",
            'verify_token': "",
            'link': ""
        }
    }

async def present_user(user_id: int):
    found = await user_data.find_one({'_id': user_id})
    return bool(found)

async def add_user(user_id: int):
    user = new_user(user_id)
    await user_data.insert_one(user)
    return

async def db_verify_status(user_id):
    user = await user_data.find_one({'_id': user_id})
    if user:
        return user.get('verify_status', default_verify)
    return default_verify

async def db_update_verify_status(user_id, verify):
    await user_data.update_one({'_id': user_id}, {'$set': {'verify_status': verify}})

async def full_userbase():
    user_docs = user_data.find()
    user_ids = [doc['_id'] async for doc in user_docs]
    return user_ids

async def del_user(user_id: int):
    await user_data.delete_one({'_id': user_id})
    return

async def save_batch_data(first_msg_id, last_msg_id, channel_id, created_by):
    data = {
        "first_msg_id": first_msg_id,
        "last_msg_id": last_msg_id,
        "channel_id": channel_id,
        "created_by": created_by,
        "timestamp": datetime.utcnow().isoformat()
    }
    batch_collection.insert_one(data)

async def get_batch_data():
    return list(batch_collection.find())