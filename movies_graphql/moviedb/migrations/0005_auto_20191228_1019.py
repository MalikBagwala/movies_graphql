# Generated by Django 3.0.1 on 2019-12-28 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moviedb', '0004_systemuser_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actor',
            name='first_name',
            field=models.CharField(blank=True, max_length=60, null=True, verbose_name='First Name'),
        ),
        migrations.AlterField(
            model_name='actor',
            name='last_name',
            field=models.CharField(blank=True, max_length=60, null=True, verbose_name='Last Name'),
        ),
    ]
