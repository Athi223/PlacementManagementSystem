# Generated by Django 3.2.6 on 2021-08-26 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Company', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='criteria',
            name='skillSet',
            field=models.TextField(null=True),
        ),
    ]