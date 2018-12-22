from django.conf.urls import include, url
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register('users', views.UserViewSet)
router.register('groups', views.GroupViewSet)

# Wire up our API using automatic URL routing.
urlpatterns = [
    url('', include(router.urls)),
]
