# Generated by Django 3.2 on 2021-06-28 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='content',
            field=models.TextField(),
        ),
    ]
