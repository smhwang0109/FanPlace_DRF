# Generated by Django 2.1.15 on 2020-06-15 12:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0004_articlecomment_author'),
    ]

    operations = [
        migrations.RenameField(
            model_name='articlecomment',
            old_name='author',
            new_name='username',
        ),
    ]