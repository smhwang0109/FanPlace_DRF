# Generated by Django 2.1.15 on 2020-06-13 12:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_auto_20200613_1715'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='title',
        ),
    ]