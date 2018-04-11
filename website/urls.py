from django.urls import path
from . import views

urlpatterns = [
    path('look/<int:int_index>/', views.look, name='look'),
    # path('edit/<int:int_index>/', views.edit, name='edit'),
    # path('delete/<int:int_index>/', views.delete, name='delete'),
    path('', views.index, name='index')
]