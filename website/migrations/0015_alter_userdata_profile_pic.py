# Generated by Django 3.2.20 on 2023-09-03 02:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0014_auto_20230903_0204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdata',
            name='profile_pic',
            field=models.CharField(default=None, max_length=350, null=True),
        ),
    ]
