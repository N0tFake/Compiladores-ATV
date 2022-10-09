from urllib.parse import urlparse
from django.urls import path
from app import views

urlpatterns = [
    path('', views.home, name='home'),
    path('form', views.expression, name='expression')
]
