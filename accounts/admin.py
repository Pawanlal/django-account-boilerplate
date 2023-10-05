from django.contrib import admin

from .models import User, HealthRecord

admin.site.register(User)
admin.site.register(HealthRecord)
