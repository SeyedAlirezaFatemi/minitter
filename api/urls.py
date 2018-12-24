from django.conf.urls import url
from rest_framework.authtoken import views

from .views import new_tweet, update_auth_token

urlpatterns = [
    url('api-token-auth/', views.obtain_auth_token),
    url('api-update-token/', update_auth_token),
    url('new-tweet/', new_tweet),
]
