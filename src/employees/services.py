import decimal

from employees.models import Employee
from django.db.models import Count, Sum


def get_counters_department(ids: list) -> dict:
    """
    Получение счетчиков для департаментов.
    Подсчет количества сотрудников и суммы оклада по департаменту.
    """
    if not ids:
        return {}
    counters = Employee.objects.values('department_id').annotate(
        num_employees=Count('id'),
        sum_salary=Sum('salary')
    ).filter(department_id__in=ids)
    counters = {counter.get('department_id'): counter for counter in counters}

    return counters


def add_counters_to_response(counters: dict, response: dict) -> None:
    """
    Добавление в json-ответ полей-счетчиков.
    """
    if counters and counters.get(response['id']):
        response['num_employees'] = counters[response['id']]['num_employees']
        response['sum_salary'] = counters[response['id']]['sum_salary']
    else:
        response['num_employees'] = 0
        response['sum_salary'] = decimal.Decimal(0)
