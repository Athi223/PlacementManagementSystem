# Generated by Django 3.2.6 on 2021-08-27 17:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Company', '0002_alter_criteria_skillset'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='companyId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Offer', to='Company.company'),
        ),
    ]
