# Generated by Django 3.2.20 on 2023-09-03 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0015_alter_userdata_profile_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='design',
            field=models.CharField(default='success', max_length=100),
        ),
    ]
