from django.urls import path
from . import views


urlpatterns = [
    path('aux_data/', views.aux_data),
    path('data/', views.process_data),
    path('data2/', views.process_data2),
    path('exists/', views.check_if_exists),
]