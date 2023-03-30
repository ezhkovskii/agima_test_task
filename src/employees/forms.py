from django import forms

from employees.models import Department, Employee


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['director', 'name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Директором можно выбрать сотрудника, который находится в выбранном департаменте
        self.fields['director'].queryset = Employee.objects.filter(
            department_id=self.instance.id)
