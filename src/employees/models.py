from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    director = models.ForeignKey("Employee", on_delete=models.SET_NULL, related_name='head', null=True, blank=True,
                                 verbose_name='Директор', unique=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Департамент'
        verbose_name_plural = 'Департаменты'


class Employee(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя')
    surname = models.CharField(max_length=255, verbose_name='Фамилия', db_index=True)
    patronymic = models.CharField(max_length=255, verbose_name='Отчество', null=True, blank=True)
    photo = models.ImageField(upload_to='photos_employees', null=True, blank=True, verbose_name='Фото')
    position = models.CharField(max_length=255, verbose_name='Должность')
    salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Оклад')
    age = models.PositiveSmallIntegerField(verbose_name='Возраст')
    department = models.ForeignKey(Department, on_delete=models.PROTECT, verbose_name='Отдел')

    def __str__(self):
        return f'{self.surname} {self.name} {self.patronymic}' if self.patronymic else f'{self.surname} {self.name}'

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
