from django.contrib import admin

from .models import UserProfile, UserPersona, UserInterests

admin.site.register(UserPersona)
admin.site.register(UserProfile)
admin.site.register(UserInterests)