# Generated by Django 5.0.3 on 2024-04-27 09:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0083_users_registration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='weight',
        ),
    ]