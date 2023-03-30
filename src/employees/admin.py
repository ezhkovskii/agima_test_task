from django.contrib import admin
from employees.models import Employee, Department
from employees.forms import DepartmentForm


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_filter = ('position', 'department')
    search_fields = ('name', 'surname', 'patronymic')


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'director')
    search_fields = ('name', 'director__name')
    form = DepartmentForm
