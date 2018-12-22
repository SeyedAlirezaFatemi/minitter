from django.contrib import admin

# Register your models here.
from .models import LoggedInUser, Profile, Tweet

admin.site.register(Tweet)
admin.site.register(Profile)
admin.site.register(LoggedInUser)
