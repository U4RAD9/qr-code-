# Generated by Django 5.0.3 on 2024-05-01 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0089_alter_users_patient_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='xrai_id',
            field=models.CharField(default='0', max_length=100),
        ),
    ]
