# Generated by Django 3.2.12 on 2022-04-09 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_customuser_uniquecode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='uniqueCode',
            field=models.UUIDField(blank=True, default='1f684ca83c814520b74fbf18d0a9cdfd', unique=True),
        ),
    ]
