from django.conf.urls import url

from rest_framework.authtoken import views

# Wire up our API using automatic URL routing.
urlpatterns = [
    url('api-token-auth/', views.obtain_auth_token),
]
