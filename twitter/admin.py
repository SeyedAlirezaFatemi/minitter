from django.contrib import admin

from .models import FailedLogInAttempt, LoggedInUser, Profile, Request, Tweet, UnAuthorizedRequests

admin.site.register(Tweet)
admin.site.register(Profile)
admin.site.register(LoggedInUser)
admin.site.register(UnAuthorizedRequests)
admin.site.register(Request)
admin.site.register(FailedLogInAttempt)
