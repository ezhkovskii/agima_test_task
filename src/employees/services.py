from employees.models import Employee
from django.db.models import Count, Sum


class DirectorException(Exception):
    ...


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
    if counters:
        response['num_employees'] = counters[response['id']]['num_employees']
        response['sum_salary'] = counters[response['id']]['sum_salary']
