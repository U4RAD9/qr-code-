# Generated by Django 5.0.3 on 2024-05-04 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0091_remove_users_drconsultation_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='drconsultation',
            field=models.BooleanField(default=False),
        ),
    ]
