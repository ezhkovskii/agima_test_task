from collections import OrderedDict
from decimal import Decimal
import json

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from employees.models import Department, Employee
from employees.exceptions import DirectorException
from employees.tests.scenarios import get_department_schema, get_employee_schema, fill_employee_random, \
    fill_employee_from_object

# создание департамента с логином и без +
# создание департамента с директором (ошибка) +
# удаление департамента с логином и без +
# изменение департамента с логином и без +
# список департаментов без логина +
# чтение департамента без логина +

# чтение департамента с сотрудниками и проверка искусственных полей с логином +
# чтение списка департамента с сотрудниками и проверка искусственных полей с логином +
# добавление директора
#     из другого департамента
#     из этого департамента
#     сотрудник уже директор в другом департаменте


# создание сотрудников с логином и без
# удаление сотрудников с логином и без
# изменение сотрудников с логином и без
# список сотрудников с логином и без
# чтение сотрудников с логином и без
# поиск по фамилии
# поиск по департаменту
# проверка пагинации


USER = 'john'
PASSWORD = 'johnpassword'
EMAIL = 'john@snow.com'


class SwaggerTests(APITestCase):

    def test_swagger_page(self):
        """Проверка страницы swagger"""
        response = self.client.get('/swagger/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DepartmentTests(APITestCase):

    def setUp(self):
        self.superuser = User.objects.create_superuser(USER, EMAIL, PASSWORD)
        self.client.login(username=USER, password=PASSWORD)

    def test_create_department(self, status_code=status.HTTP_201_CREATED):
        """Создание департамента с авторизацией"""

        data = {'name': 'Department1'}
        response = self.client.post('/api/departments/', data, format='json')
        self.assertEqual(response.status_code, status_code)
        if response.status_code == status.HTTP_201_CREATED:
            expected_response = get_department_schema(add_counters=False)
            expected_response['id'] = 1
            expected_response['name'] = data['name']
            self.assertEqual(response.data, expected_response)

    def test_create_department_without_login(self):
        """Создание департамента без авторизации"""
        self.client.logout()
        self.test_create_department(status.HTTP_403_FORBIDDEN)

    def test_create_department_with_director(self):
        """Создание департамента вместе с присвоением ему директора"""
        self.client.login(username=USER, password=PASSWORD)

        dep = Department.objects.create(name='Department1')
        emp = get_employee_schema()
        emp = fill_employee_random(emp)
        emp.pop('id')
        emp['department'] = dep
        emp = Employee.objects.create(**emp)
        dep.director = emp
        dep.save()

        data = {'name': 'Department2', 'director': emp.id}
        response = self.client.post('/api/departments/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {
                "director": [
                    "Департамент с таким Директор уже существует."
                ]
            })

    def test_get_department_without_login(self):
        """Чтение департамента без логина"""
        self.client.logout()
        dep = Department.objects.create(name='Department1')
        response = self.client.get(f'/api/departments/{dep.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_response = get_department_schema()
        expected_response['id'] = dep.id
        expected_response['name'] = dep.name
        self.assertEqual(response.data, expected_response)

    def test_get_departments_without_login(self):
        """Чтение списка департаментов без логина"""
        self.client.logout()
        dep1 = Department.objects.create(name='Department1')
        dep2 = Department.objects.create(name='Department2')
        response = self.client.get(f'/api/departments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        dep_schema1 = get_department_schema()
        dep_schema2 = get_department_schema()
        dep_schema1['id'] = dep1.id
        dep_schema1['name'] = dep1.name
        dep_schema2['id'] = dep2.id
        dep_schema2['name'] = dep2.name
        expected_response = [dep_schema1, dep_schema2]
        self.assertEqual(response.data, expected_response)

    def test_get_department_with_employees(self):
        """Чтение департамента с сотрудниками и проверка искусственных полей"""
        dep = Department.objects.create(name='Department1')
        emp = get_employee_schema()
        emp = fill_employee_random(emp)
        emp.pop('id')
        emp['department'] = dep
        emp1 = Employee.objects.create(**emp)
        emp.update({'name': 'Name2'})
        emp2 = Employee.objects.create(**emp)

        response = self.client.get(f'/api/departments/{dep.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        emp_schema1 = get_employee_schema()
        emp_schema1 = fill_employee_from_object(emp_schema1, emp1)
        emp_schema2 = get_employee_schema()
        emp_schema2 = fill_employee_from_object(emp_schema2, emp2)
        employees = [emp_schema1, emp_schema2]

        expected_response = get_department_schema()
        expected_response['id'] = dep.id
        expected_response['name'] = dep.name
        expected_response['employees'] = employees
        expected_response['num_employees'] = len(employees)
        expected_response['sum_salary'] = sum(Decimal(employee['salary']) for employee in employees)

        self.assertEqual(response.data, expected_response)

    def test_get_departments_with_employees(self):
        """Чтение списка департаментов с сотрудниками и проверка искусственных полей"""
        dep1 = Department.objects.create(name='Department1')
        dep2 = Department.objects.create(name='Department2')
        emp = get_employee_schema()
        emp = fill_employee_random(emp)
        emp.pop('id')
        emp['department'] = dep1
        emp1 = Employee.objects.create(**emp)
        emp.update({'name': 'Name2'})
        emp2 = Employee.objects.create(**emp)
        response = self.client.get(f'/api/departments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        emp_schema1 = get_employee_schema()
        emp_schema1 = fill_employee_from_object(emp_schema1, emp1)
        emp_schema2 = get_employee_schema()
        emp_schema2 = fill_employee_from_object(emp_schema2, emp2)
        employees = [emp_schema1, emp_schema2]

        dep_schema1 = get_department_schema()
        dep_schema1['id'] = dep1.id
        dep_schema1['name'] = dep1.name
        dep_schema1['employees'] = employees
        dep_schema1['num_employees'] = len(employees)
        dep_schema1['sum_salary'] = sum(Decimal(employee['salary']) for employee in employees)

        dep_schema2 = get_department_schema()
        dep_schema2['id'] = dep2.id
        dep_schema2['name'] = dep2.name
        expected_response = [dep_schema1, dep_schema2]

        self.assertEqual(response.data, expected_response)

    def test_delete_department(self, status_code=status.HTTP_204_NO_CONTENT):
        """Удаление департамента"""
        dep = Department.objects.create(name='Department1')
        response = self.client.delete(f'/api/departments/{dep.id}/')
        self.assertEqual(response.status_code, status_code)
        if response.status_code == status.HTTP_204_NO_CONTENT:
            self.assertRaises(Department.DoesNotExist, Department.objects.get, id=dep.id)

    def test_delete_department_without_login(self):
        """Удаление департамента без логина"""
        self.client.logout()
        self.test_delete_department(status.HTTP_403_FORBIDDEN)

    def test_update_department(self, status_code=status.HTTP_200_OK):
        """Изменение департамента"""
        dep = Department.objects.create(name='Department1')
        data = {'name': 'Department2'}
        response = self.client.patch(f'/api/departments/{dep.id}/', data, format='json')
        self.assertEqual(response.status_code, status_code)
        if response.status_code == status.HTTP_200_OK:
            self.assertEqual(response.data['name'], data['name'])

    def test_update_department_without_login(self):
        """Изменение департамента без логина"""
        self.client.logout()
        self.test_update_department(status.HTTP_403_FORBIDDEN)
