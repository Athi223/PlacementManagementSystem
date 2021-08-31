from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import DateField, TextField, FloatField, IntegerField
from Company.models import Offer

# Create your models here.
class Student(models.Model):
	studentId = models.OneToOneField(User, on_delete=models.CASCADE, related_name='Student')
	prn = models.TextField()
	phoneNumber = TextField(default='')
	dob = DateField(null=True)
	department = TextField(default='')
	verificationStatus = IntegerField(default=0)			# 0: Not Filled, 1: Accepted, 2: Rejected, 3: Pending
	placedOffer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name='PlacedOffer', null=True)

class Eligibility(models.Model):
	studentId = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='Eligibility')
	cgpa = FloatField(null=True)
	liveBacklog = IntegerField(null=True)
	deadBacklog = IntegerField(null=True)
	passingYear = IntegerField(null=True)
	yearGap = IntegerField(null=True)
	skillSet = TextField(default='')