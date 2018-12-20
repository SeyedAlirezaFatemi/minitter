from django.urls import path

from . import views
from django.urls import path, include
from django.views.generic.base import TemplateView

urlpatterns = [
    path('auth/', include('django.contrib.auth.urls')),
    path('', TemplateView.as_view(template_name='home.html'), name='twitter'),
]
