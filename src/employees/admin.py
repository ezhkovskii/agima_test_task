from django.contrib import admin
from employees.models import Employee, Department


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_filter = ['position', 'department']
    search_fields = ('name', 'surname', 'patronymic')


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Директором можно выбрать сотрудника, который находится в выбранном департаменте"""
        if db_field.name == "director":
            kwargs["queryset"] = Employee.objects.filter(department=int(request.resolver_match.kwargs['object_id']))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

