"""
Data URLs
"""

from django.urls import path

from . import views

urlpatterns = [
    path('', views.receive_data, name='receive_data'),
]