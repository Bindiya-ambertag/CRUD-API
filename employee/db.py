from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["employee_db"]
employee_collection = db["employees"]
users_collection = db["users"]
