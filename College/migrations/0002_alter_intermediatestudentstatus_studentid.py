# Generated by Django 3.2.6 on 2021-08-27 17:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0001_initial'),
        ('College', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='intermediatestudentstatus',
            name='studentId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Student.student'),
        ),
    ]
