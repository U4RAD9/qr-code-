# Generated by Django 3.1.3 on 2023-12-05 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0073_auto_20231202_1722'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='currect_time',
            field=models.CharField(default=None, max_length=100),
        ),
    ]
