from django.contrib import admin
from .models import Doctor
from accounts.models import Patient, Session

admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Session)
# Register your models here.
