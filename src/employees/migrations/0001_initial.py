# Generated by Django 4.1.7 on 2023-03-28 07:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Департамент',
                'verbose_name_plural': 'Департаменты',
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Имя')),
                ('surname', models.CharField(db_index=True, max_length=255, verbose_name='Фамилия')),
                ('patronymic', models.CharField(blank=True, max_length=255, null=True, verbose_name='Отчество')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='photos_employees', verbose_name='Фото')),
                ('position', models.CharField(max_length=255, verbose_name='Должность')),
                ('salary', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Оклад')),
                ('age', models.PositiveSmallIntegerField(verbose_name='Возраст')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='employees.department', verbose_name='Отдел')),
            ],
            options={
                'verbose_name': 'Сотрудник',
                'verbose_name_plural': 'Сотрудники',
            },
        ),
        migrations.AddField(
            model_name='department',
            name='director',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='head', to='employees.employee', unique=True, verbose_name='Директор'),
        ),
    ]
