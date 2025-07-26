from bson.objectid import ObjectId
from app.server.database.connection import user_collection

# helpers
def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "fullname": user["fullname"],
        "email": user["email"],
        "password": user["password"],
    }

# Add a new user into to the database
def add_user(user_data: dict) -> dict:
    user = user_collection.insert_one(user_data)
    new_user = user_collection.find_one({"_id": user.inserted_id})
    return user_helper(new_user)

# Retrieve all users present in the database
def retrieve_users():
    users = []
    user_query=user_collection.find()
    for student in user_query:
        users.append(user_helper(student))
    return users

# Retrieve a user with a matching email
def retrieve_user(email: dict) -> dict:
    user = user_collection.find_one({"email": email})
    if user:
        return user_helper(user)

# Retrieve a student with a matching ID
def login_user(id: str) -> dict:
    user = user_collection.find_one({"_id": ObjectId(id)})
    if user:
        return user_helper(user)