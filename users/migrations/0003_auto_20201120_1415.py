# Generated by Django 3.1.1 on 2020-11-20 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20201120_1349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='city',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='user',
            name='country',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='user',
            name='interests',
            field=models.TextField(default='', max_length=255),
        ),
    ]
