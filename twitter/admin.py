from django.contrib import admin

# Register your models here.
from .models import LoggedInUser, Profile, Tweet, UnAuthorizedRequests, Request, FailedLogInAttempt

admin.site.register(Tweet)
admin.site.register(Profile)
admin.site.register(LoggedInUser)
admin.site.register(UnAuthorizedRequests)
admin.site.register(Request)
admin.site.register(FailedLogInAttempt)
