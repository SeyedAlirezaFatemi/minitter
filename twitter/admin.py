from django.contrib import admin

# Register your models here.
from .models import Profile, Tweet, LoggedInUser

admin.site.register(Tweet)
admin.site.register(Profile)
admin.site.register(LoggedInUser)
