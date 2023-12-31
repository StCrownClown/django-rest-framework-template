# Generated by Django 4.2.5 on 2023-10-09 08:00

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='citizen_id',
            field=models.CharField(max_length=13, unique=True, validators=[django.core.validators.RegexValidator('^\\d{13}$', 'Citizen ID must be exactly 13 digits long and only contain numbers.')]),
        ),
        migrations.AlterField(
            model_name='customer',
            name='mobile',
            field=models.CharField(max_length=10, validators=[django.core.validators.RegexValidator('^\\d{10}$', 'Mobile number must be exactly 10 digits long and only contain numbers.')]),
        ),
    ]
