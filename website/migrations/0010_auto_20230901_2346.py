# Generated by Django 3.2.20 on 2023-09-01 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0009_auto_20230901_2342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdata',
            name='first_name',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='userdata',
            name='github_link',
            field=models.CharField(default=None, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='userdata',
            name='last_name',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='userdata',
            name='profile_pic',
            field=models.CharField(default=None, max_length=200, null=True),
        ),
    ]
