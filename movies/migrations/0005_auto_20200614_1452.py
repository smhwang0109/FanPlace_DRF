# Generated by Django 2.1.15 on 2020-06-14 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0004_auto_20200614_1449'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='overview',
            field=models.TextField(blank=True, null=True),
        ),
    ]
