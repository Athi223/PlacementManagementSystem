# Generated by Django 3.2.6 on 2021-08-28 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('College', '0002_alter_intermediatestudentstatus_studentid'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentinfo',
            name='department',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='studentinfo',
            name='passingYear',
            field=models.IntegerField(default=2021),
            preserve_default=False,
        ),
    ]
