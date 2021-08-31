from django.contrib import admin
from .models import Company, Criteria, Offer

# Register your models here.
admin.site.register(Company)
admin.site.register(Offer)
admin.site.register(Criteria)