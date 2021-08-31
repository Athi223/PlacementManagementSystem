from django.contrib import admin
from .models import Eligibility, Student

# Register your models here.
admin.site.register(Student)
admin.site.register(Eligibility)