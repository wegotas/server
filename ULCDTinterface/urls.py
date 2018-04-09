from django.urls import path
from . import views


urlpatterns = [
    path('aux_data/', views.aux_data),
    path('data/', views.process_data),
]