# Generated by Django 3.1.1 on 2020-11-20 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='city',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='country',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='interests',
            field=models.TextField(max_length=255, null=True),
        ),
    ]