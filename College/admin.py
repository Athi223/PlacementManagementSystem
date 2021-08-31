from College.models import IntermediateStudentStatus
from django.contrib import admin
from .models import College, StudentInfo, IntermediateStudentStatus

# Register your models here.
admin.site.register(College)
admin.site.register(StudentInfo)
admin.site.register(IntermediateStudentStatus)