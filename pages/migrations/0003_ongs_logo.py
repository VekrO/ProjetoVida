# Generated by Django 4.1.2 on 2022-10-05 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_alter_ongs_nome_responsavel'),
    ]

    operations = [
        migrations.AddField(
            model_name='ongs',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]