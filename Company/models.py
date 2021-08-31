from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import DateField, IntegerField, TextField, FloatField
from django.db.models.fields.related import ForeignKey

# Create your models here.
class Company(models.Model):
	companyId = models.OneToOneField(User, on_delete=models.CASCADE, related_name='Company')
	phoneNumber = TextField(default='')

class Offer(models.Model):
	companyId = ForeignKey(Company, on_delete=models.CASCADE, related_name='Offer')
	jobRole = TextField()
	jobLocation = TextField()
	bond = IntegerField()
	deadline = DateField()
	package = IntegerField()
	acceptedStudents = TextField()

class Criteria(models.Model):
	offerId = models.OneToOneField(Offer, on_delete=models.CASCADE, related_name='Criteria')
	cgpa = FloatField()
	liveBacklog = IntegerField()
	deadBacklog = IntegerField()
	passingYear = IntegerField()
	yearGap = IntegerField()
	skillSet = TextField(null=True)
