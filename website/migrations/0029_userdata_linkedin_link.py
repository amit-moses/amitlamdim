# Generated by Django 3.2.20 on 2023-09-04 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0028_resume'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdata',
            name='linkedin_link',
            field=models.CharField(default=None, max_length=300, null=True),
        ),
    ]