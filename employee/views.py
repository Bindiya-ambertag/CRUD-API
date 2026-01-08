from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from bson import ObjectId
from .db import employee_collection
from .serializers import EmployeeSerializer

# Create your views here.
@api_view(['GET', 'POST'])
def employee_list(request):

    if request.method == 'GET':
        employees = list(employee_collection.find())
        for emp in employees:
            emp['_id'] = str(emp['_id'])
        return Response(employees)

    if request.method == 'POST':

        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            employee_collection.insert_one(serializer.validated_data)
            return Response({'message': 'Employee created'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def employee_detail(request, id):

    employee = employee_collection.find_one({'_id': ObjectId(id)})
    if not employee:
        return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        employee['_id'] = str(employee['_id'])
        return Response(employee)

    if request.method == 'PUT':
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            employee_collection.update_one(
                {'_id': ObjectId(id)},
                {'$set': serializer.validated_data}
            )
            return Response({'message': 'Employee updated'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        employee_collection.delete_one({'_id': ObjectId(id)})
        return Response({'message': 'Employee deleted'})