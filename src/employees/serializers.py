from rest_framework import serializers

from employees.models import Employee, Department
from employees.exceptions import DirectorException, DIRECTOR_ERROR


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):
    employees = EmployeeSerializer(many=True, read_only=True)

    def create(self, validated_data):
        if validated_data.get('director'):
            raise DirectorException(DIRECTOR_ERROR)

        return super().create(validated_data)

    def update(self, instance, validated_data):
        if validated_data.get('director'):
            if instance.id != validated_data['director'].department_id:
                raise DirectorException(DIRECTOR_ERROR)

        response = super().update(instance, validated_data)
        return response

    class Meta:
        model = Department
        fields = '__all__'
