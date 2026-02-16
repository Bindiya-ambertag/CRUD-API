# from django.shortcuts import render
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status
# from bson import ObjectId
# from .db import employee_collection
# from .serializers import EmployeeSerializer
#
# # Create your views here.
# @api_view(['GET', 'POST'])
# def employee_list(request):
#
#     if request.method == 'GET':
#         employees = list(employee_collection.find())
#         for emp in employees:
#             emp['_id'] = str(emp['_id'])
#         return Response(employees)
#
#     if request.method == 'POST':
#
#         serializer = EmployeeSerializer(data=request.data)
#         if serializer.is_valid():
#             employee_collection.insert_one(serializer.validated_data)
#             return Response({'message': 'Employee created'}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def employee_detail(request, id):
#
#     employee = employee_collection.find_one({'_id': ObjectId(id)})
#     if not employee:
#         return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'GET':
#         employee['_id'] = str(employee['_id'])
#         return Response(employee)
#
#     if request.method == 'PUT':
#         serializer = EmployeeSerializer(data=request.data)
#         if serializer.is_valid():
#             employee_collection.update_one(
#                 {'_id': ObjectId(id)},
#                 {'$set': serializer.validated_data}
#             )
#             return Response({'message': 'Employee updated'})
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     if request.method == 'DELETE':
#         employee_collection.delete_one({'_id': ObjectId(id)})
#         return Response({'message': 'Employee deleted'})
#
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# import logging
# from .serializers import EmployeeSerializer
# from . import queries
# from django.shortcuts import render
#
# logger = logging.getLogger(__name__)
#
# class EmployeeListView(APIView):
#
#     def get(self, request):
#         logger.info("GET /employees called by user=%s", request.user)
#         employees = queries.get_all_employees()
#         logger.debug("Employees fetched count=%s", len(employees))
#         return Response(employees)
#
#     def post(self, request):
#         logger.info("POST /employees called by user=%s", request.user)
#         serializer = EmployeeSerializer(data=request.data)
#         if serializer.is_valid():
#             emp_id = queries.create_employee(serializer.validated_data)
#             logger.info("Employee created successfully with id=%s", emp_id)
#             return Response(
#                 {"message": "Employee created", "id": emp_id},
#                 status=status.HTTP_201_CREATED
#             )
#
#         logger.warning("Employee creation failed: %s", serializer.errors)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class EmployeeDetailView(APIView):
#
#     def get(self, request, id):
#         logger.info("GET /employees/%s called by user=%s", id, request.user)
#         employee = queries.get_employee_by_id(id)
#         if not employee:
#             logger.warning("Employee not found id=%s", id)
#             return Response({"error": "Employee not found"}, status=404)
#         return Response(employee)
#
#     def put(self, request, id):
#         logger.info("PUT /employees/%s called by user=%s", id, request.user)
#
#         serializer = EmployeeSerializer(data=request.data)
#         if serializer.is_valid():
#             updated = queries.update_employee(id, serializer.validated_data)
#             logger.info("Employee updated id=%s", id)
#             return Response(updated)
#         logger.warning("Employee update failed id=%s errors=%s", id, serializer.errors)
#         return Response(serializer.errors, status=400)
#
#     def delete(self, request, id):
#         logger.info("DELETE /employees/%s called by user=%s", id, request.user)
#         deleted = queries.delete_employee(id)
#         if deleted:
#             logger.info("Employee deleted id=%s", id)
#             return Response({"message": "Employee deleted"})
#         logger.warning("Employee delete failed, not found id=%s", id)
#         return Response({"error": "Employee not found"}, status=404)
#
# def employee_page(request):
#     logger.info("Employee page accessed by user=%s", request.user)
#     employees = queries.get_all_employees()  # reuse existing logic
#     return render(
#         request,
#         "employee/employee_list.html",
#         {"employees": employees}
#     )

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import logging
import base64
from rest_framework.permissions import AllowAny
from rest_framework.authentication import BasicAuthentication, SessionAuthentication

from .serializers import EmployeeSerializer
from . import queries
from django.shortcuts import render
from .user_queries import authenticate_user   # MongoDB user authentication

logger = logging.getLogger(__name__)


# ----------- Basic Auth Function (MongoDB) -----------
def basic_authenticate(request):
    auth_header = request.META.get("HTTP_AUTHORIZATION")

    if not auth_header:
        return None

    try:
        auth_type, credentials = auth_header.split()

        if auth_type.lower() != "basic":
            return None

        decoded = base64.b64decode(credentials).decode("utf-8")
        username, password = decoded.split(":")

        user = authenticate_user(username, password)
        return user

    except Exception:
        return None


# ---------------- Employee List ----------------
class EmployeeListView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        user = basic_authenticate(request)
        if not user:
            logger.warning("Unauthorized GET /employees attempt")
            return Response({"error": "Invalid username or password"}, status=401)

        logger.info("GET /employees called by user=%s", user["username"])
        employees = queries.get_all_employees()
        logger.debug("Employees fetched count=%s", len(employees))
        return Response(employees)

    def post(self, request):
        user = basic_authenticate(request)
        if not user:
            logger.warning("Unauthorized POST /employees attempt")
            return Response({"error": "Invalid username or password"}, status=401)

        logger.info("POST /employees called by user=%s", user["username"])
        serializer = EmployeeSerializer(data=request.data)

        if serializer.is_valid():
            emp_id = queries.create_employee(serializer.validated_data)
            logger.info("Employee created successfully with id=%s", emp_id)
            return Response(
                {"message": "Employee created", "id": emp_id},
                status=status.HTTP_201_CREATED
            )

        logger.warning("Employee creation failed: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ---------------- Employee Detail ----------------
class EmployeeDetailView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request, id):
        user = basic_authenticate(request)
        if not user:
            logger.warning("Unauthorized GET /employees/%s attempt", id)
            return Response({"error": "Invalid username or password"}, status=401)

        logger.info("GET /employees/%s called by user=%s", id, user["username"])
        employee = queries.get_employee_by_id(id)
        if not employee:
            logger.warning("Employee not found id=%s", id)
            return Response({"error": "Employee not found"}, status=404)
        return Response(employee)

    def put(self, request, id):
        user = basic_authenticate(request)
        if not user:
            logger.warning("Unauthorized PUT /employees/%s attempt", id)
            return Response({"error": "Invalid username or password"}, status=401)

        logger.info("PUT /employees/%s called by user=%s", id, user["username"])
        serializer = EmployeeSerializer(data=request.data)

        if serializer.is_valid():
            updated = queries.update_employee(id, serializer.validated_data)
            logger.info("Employee updated id=%s", id)
            return Response(updated)

        logger.warning("Employee update failed id=%s errors=%s", id, serializer.errors)
        return Response(serializer.errors, status=400)

    def delete(self, request, id):
        user = basic_authenticate(request)
        if not user:
            logger.warning("Unauthorized DELETE /employees/%s attempt", id)
            return Response({"error": "Invalid username or password"}, status=401)

        logger.info("DELETE /employees/%s called by user=%s", id, user["username"])
        deleted = queries.delete_employee(id)
        if deleted:
            logger.info("Employee deleted id=%s", id)
            return Response({"message": "Employee deleted"})
        logger.warning("Employee delete failed, not found id=%s", id)
        return Response({"error": "Employee not found"}, status=404)


# ---------------- Web Page ----------------
def employee_page(request):
    logger.info("Employee page accessed by user=%s", request.user)
    employees = queries.get_all_employees()
    return render(
        request,
        "employee/employee_list.html",
        {"employees": employees}
    )
