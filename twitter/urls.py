from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.twitter, name='twitter'),
    path('auth/', include('django.contrib.auth.urls')),
    path('upload_avatar/', views.upload_avatar, name='upload_avatar'),
    path('new_tweet/', views.new_tweet, name='new_tweet'),
    path('signup/', views.SignUp.as_view(), name='signup'),
]
