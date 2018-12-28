from django.conf.urls import url

from . import views

urlpatterns = [
    url('api-token-auth/', views.CustomAuthToken.as_view()),
    url('api-update-token/', views.update_auth_token, name='update_token'),
    url('new-tweet/', views.new_tweet, name='new_tweet'),
]

app_name = 'api'
