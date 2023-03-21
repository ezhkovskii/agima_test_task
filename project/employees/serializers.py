from functools import lru_cache

from django.db.models import Count, Sum
from rest_framework import serializers

from employees.models import Employee, Department


class EmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        info = Employee.objects.values('department_id').annotate(num_employees=Count('id'), sum_salary=Sum('salary')).filter(department_id=instance.id)[0]
        representation['num_employees'] = info.get('num_employees')
        representation['sum_salary'] = info.get('sum_salary')

        return representation

    class Meta:
        model = Department
        fields = '__all__'
