# Generated by Django 4.1.2 on 2022-10-08 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_rename_admin_user_is_admin_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_org',
            field=models.BooleanField(default=False),
        ),
    ]
