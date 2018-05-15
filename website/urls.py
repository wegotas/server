from django.urls import path
from . import views

urlpatterns = [
    path('look/<int:int_index>/', views.look, name='look'),
    path('edit/<int:int_index>/', views.edit, name='edit'),
    path('delete/<int:int_index>/', views.delete, name='delete'),
    path('mass_delete/', views.mass_delete, name='mass_delete'),
    path('mass_excel/', views.mass_excel, name='mass_excel'),
    path('cat_change/', views.cat_change, name='cat_change'),
    path('', views.index, name='index')
]