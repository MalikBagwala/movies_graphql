# Generated by Django 2.1.3 on 2019-12-08 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moviedb', '0004_auto_20191207_0807'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='budget',
            field=models.FloatField(blank=True, null=True),
        ),
    ]