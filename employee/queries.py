from bson import ObjectId
from .db import employee_collection


def get_all_employees():
    employees = list(employee_collection.find())
    for emp in employees:
        emp['_id'] = str(emp['_id'])
    return employees


def get_employee_by_id(emp_id):
    employee = employee_collection.find_one({"_id": ObjectId(emp_id)})
    if employee:
        employee['_id'] = str(employee['_id'])
    return employee


def create_employee(data):
    result = employee_collection.insert_one(data)
    return str(result.inserted_id)


def update_employee(emp_id, data):
    employee_collection.update_one(
        {"_id": ObjectId(emp_id)},
        {"$set": data}
    )
    return get_employee_by_id(emp_id)


def delete_employee(emp_id):
    result = employee_collection.delete_one({"_id": ObjectId(emp_id)})
    return result.deleted_count > 0
