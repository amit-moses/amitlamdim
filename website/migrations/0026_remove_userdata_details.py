# Generated by Django 3.2.20 on 2023-09-03 18:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0025_userdata_details'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userdata',
            name='details',
        ),
    ]
