# Generated by Django 3.1.3 on 2023-10-14 09:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0041_modalities_optometry'),
    ]

    operations = [
        migrations.RenameField(
            model_name='modalities',
            old_name='patientID',
            new_name='patient_id',
        ),
        migrations.RenameField(
            model_name='users',
            old_name='patientID',
            new_name='patient_id',
        ),
    ]
