from rest_framework import serializers
from employees.models import Employee, Department
from employees.services import DirectorException


class EmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):

    def update(self, instance, validated_data):
        if validated_data.get('director'):
            if instance.id != validated_data['director'].department_id:
                raise DirectorException('Нельзя выбрать директором сотрудника из другого отдела')

        response = super().update(instance, validated_data)
        return response

    class Meta:
        model = Department
        fields = '__all__'
