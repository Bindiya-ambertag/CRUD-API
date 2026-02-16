from django.contrib.auth.hashers import make_password, check_password
from .db import users_collection


def create_user(username, password):
    users_collection.insert_one({
        "username": username,
        "password": make_password(password)
    })


def authenticate_user(username, password):
    user = users_collection.find_one({"username": username})
    if user and check_password(password, user["password"]):
        return user
    return None
