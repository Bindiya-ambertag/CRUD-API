from rest_framework import serializers

class EmployeeSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    designation = serializers.CharField(max_length=100)
    salary = serializers.IntegerField()
