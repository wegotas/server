from django.urls import path
from . import views


urlpatterns = [
    path('aux_data/', views.aux_data),
    path('data/', views.process_data),
    path('exists/', views.check_if_exists),
    path('pictures/<int:int_index>/', views.process_pictures),
]