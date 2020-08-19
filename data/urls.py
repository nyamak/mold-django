"""
Data URLs
"""

from django.urls import path

from . import views

urlpatterns = [
    path(r'data/', views.receive_data, name='receive_data'),
    path(r'dashboard/<str:device_eui>/', views.device_dashboard, name='v')
]
