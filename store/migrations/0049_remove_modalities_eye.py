# Generated by Django 3.1.3 on 2023-10-25 05:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0048_remove_users_patient_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='modalities',
            name='eye',
        ),
    ]
