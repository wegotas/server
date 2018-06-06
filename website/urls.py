from django.urls import path
from . import views

urlpatterns = [
    path('look/<int:int_index>/', views.look, name='look'),
    path('edit/<int:int_index>/', views.edit, name='edit'),
    path('edit_order/<int:int_index>/', views.edit_order, name='edit_order'),
    path('delete/<int:int_index>/', views.delete, name='delete'),
    path('mass_delete/', views.mass_delete, name='mass_delete'),
    path('mass_excel/', views.mass_excel, name='mass_excel'),
    path('cat_change/', views.cat_change, name='cat_change'),
    path('ord_assign/', views.ord_assign, name='ord_assign'),
    path('new_record/', views.new_record, name='new_record'),
    path('new_order/', views.new_order, name='new_order'),
    path('cat/del/<int:int_index>/', views.delCat, name='categoryDeletion'),
    path('cat/edit/', views.cat_edit, name='categoryEdit'),
    path('cat/', views.categories, name='categories'),
    path('typ/del/<int:int_index>/', views.delTyp, name='typeDeletion'),
    path('typ/edit/', views.typ_edit, name='typeEdit'),
    path('typ/', views.types, name='types'),
    path('test/del/<int:int_index>/', views.delTes, name='testerDeletion'),
    path('test/edit/', views.tes_edit, name='testEdit'),
    path('test/', views.testers, name='testers'),
    path('cat_to_sold/', views.cat_to_sold, name='cat_to_sold'),
    path('', views.index, name='index')
]