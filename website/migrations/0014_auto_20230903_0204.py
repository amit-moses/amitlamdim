# Generated by Django 3.2.20 on 2023-09-03 02:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0013_rename_user_to_userexpertise_userdata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdata',
            name='background',
            field=models.CharField(default=None, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='userdata',
            name='github_link',
            field=models.CharField(default=None, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='userdata',
            name='profile_pic',
            field=models.CharField(default=None, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='userdata',
            name='website',
            field=models.CharField(default=None, max_length=300, null=True),
        ),
    ]