from rest_framework import routers

from employees.api import EmployeeViewSet, DepartmentViewSet

router = routers.DefaultRouter()
router.register(r'employees', EmployeeViewSet)
router.register(r'departments', DepartmentViewSet, 'departments')
