# Generated by Django 3.2.6 on 2021-08-26 15:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Company', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prn', models.TextField(unique=True)),
                ('cgpa', models.FloatField()),
                ('liveBacklog', models.IntegerField()),
                ('deadBacklog', models.IntegerField()),
                ('yearGap', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='IntermediateStudentStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(default=0)),
                ('offerId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Company.offer')),
                ('studentId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='College',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('email', models.EmailField(max_length=254)),
                ('phoneNumber', models.TextField()),
                ('collegeId', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='College', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
