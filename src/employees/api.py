import logging

from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from employees.models import Employee, Department
from employees.serializers import EmployeeSerializer, DepartmentSerializer
from employees.services import get_counters_department, add_counters_to_response


class StandardPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['surname', 'department']
    permission_classes = [IsAuthenticated]
    pagination_class = StandardPagination


class DepartmentViewSet(viewsets.ModelViewSet):
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        self.queryset = Department.objects.prefetch_related('employees').all()
        return self.queryset

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        department_ids = [response.data['id']]
        counters = get_counters_department(department_ids)
        add_counters_to_response(counters, response.data)

        return response

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        department_ids = [dep.get('id') for dep in response.data]
        counters = get_counters_department(department_ids)
        for resp in response.data:
            add_counters_to_response(counters, resp)

        return response





