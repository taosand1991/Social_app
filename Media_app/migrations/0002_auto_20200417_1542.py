# Generated by Django 3.0.5 on 2020-04-17 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Media_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
    ]
