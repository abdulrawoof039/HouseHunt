# Generated by Django 3.2 on 2021-06-17 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_property_is_favourite'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='property',
            name='is_favourite',
        ),
        migrations.AddField(
            model_name='accountuser',
            name='is_favourite',
            field=models.BooleanField(default=False),
        ),
    ]
