import random
import string
from collections import OrderedDict
from copy import deepcopy
from decimal import Decimal

from employees.models import Employee


def get_department_schema(add_counters: bool = True) -> dict:
    schema = {
        'id': 0,
        'employees': [],
        'name': '',
        'director': None,
        'num_employees': 0,
        'sum_salary': Decimal(0)
    }
    if not add_counters:
        schema.pop('num_employees')
        schema.pop('sum_salary')

    return OrderedDict(schema)


def get_employee_schema() -> dict:
    return OrderedDict({
        'id': 0,
        'name': '',
        'surname': '',
        'patronymic': '',
        'photo': None, 
        'position': '',
        'salary': '',
        'age': 0,
        'department': 0
    })


def get_random_string(k: int) -> str:
    return ''.join(random.choices(string.ascii_uppercase, k=k))


def fill_employee_random(emp: dict) -> dict:
    result_emp = deepcopy(emp)
    result_emp['name'] = get_random_string(10)
    result_emp['surname'] = get_random_string(10)
    result_emp['patronymic'] = get_random_string(10)
    result_emp['photo'] = None
    result_emp['position'] = get_random_string(10)
    result_emp['salary'] = '10.25'
    result_emp['age'] = 10

    return result_emp


def fill_employee_from_object(emp: dict, obj: Employee) -> dict:
    result_emp = deepcopy(emp)
    result_emp['id'] = obj.id
    result_emp['name'] = obj.name
    result_emp['surname'] = obj.surname
    result_emp['patronymic'] = obj.patronymic
    result_emp['photo'] = obj.photo or None
    result_emp['position'] = obj.position
    result_emp['salary'] = obj.salary
    result_emp['age'] = obj.age,  # почему то в age присваивается tuple, хотя тип у obj.age int
    result_emp['age'] = result_emp['age'][0]
    result_emp['department'] = obj.department.id

    return result_emp
