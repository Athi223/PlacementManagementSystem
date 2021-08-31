from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import EmailField, FloatField, IntegerField, TextField
from django.db.models.fields.related import ForeignKey
from django.contrib.auth.models import User
from Student.models import Student
from Company.models import Offer

# Create your models here.
class College(models.Model):
	collegeId = models.OneToOneField(User, on_delete=CASCADE, related_name='College')
	name = TextField()
	email = EmailField()
	phoneNumber = TextField()
	
class StudentInfo(models.Model):
	prn = TextField(unique=True)
	cgpa = FloatField()
	liveBacklog = IntegerField()
	deadBacklog = IntegerField()
	passingYear = IntegerField()
	yearGap = IntegerField()
	department = TextField()

class IntermediateStudentStatus(models.Model):
	studentId = ForeignKey(Student, on_delete=models.CASCADE)
	offerId = ForeignKey(Offer, on_delete=models.CASCADE)
	status = IntegerField(default=0)									# 0 - Pending, 1 - Accepted, 2 - Rejected