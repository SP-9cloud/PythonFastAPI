#import motor.motor_asyncio
from pymongo import MongoClient
from decouple import config

#client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
#database = client.students
#student_collection = database.get_collection("students_collection")
client = MongoClient(config("MONGO_DETAILS"))
db = client.students
student_collection = db["students_collection"]
user_collection = db["users_collection"]