# Generated by Django 3.2.12 on 2022-04-09 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20220219_1954'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='uniqueCode',
            field=models.UUIDField(blank=True, default='3a016fef8df9464391b0a0314bc1053d', unique=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='wallet',
            field=models.FloatField(default=100000.0),
        ),
    ]