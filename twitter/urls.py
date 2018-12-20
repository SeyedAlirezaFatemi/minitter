from django.urls import include, path

from . import views

urlpatterns = [
    path('auth/', include('django.contrib.auth.urls')),
    path('', views.twitter, name='twitter'),
]
