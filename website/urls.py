from django.urls import path
from . import views
from .logic import on_start

urlpatterns = [
    path('look/<int:int_index>/', views.look, name='look'),
    path('edit/<int:int_index>/', views.edit, name='edit'),
    path('by_serial/<slug:serial>/', views.edit_by_serial, name='edit_by_serial'),
    path('serial/<slug:serial>/', views.serial_processing, name='edit_by_serial'),
    path('edit_order/<int:int_index>/', views.edit_order, name='edit_order'),
    path('strip_order/<int:int_index>/', views.strip_order, name='strip_order'),
    path('delete/<int:int_index>/', views.delete, name='delete'),
    path('mass_delete/', views.mass_delete, name='mass_delete'),
    path('mass_excel/', views.mass_excel, name='mass_excel'),
    path('mass_csv/', views.mass_csv, name='mass_csv'),
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
    path('hdd_edit/<int:int_index>/', views.hdd_edit, name='hdd_edit'),
    path('hdd_delete/<int:int_index>/', views.hdd_delete, name='hdd_delete'),
    path('view_pdf/<int:int_index>/', views.view_pdf, name='view_pdf'),
    path('hdd_order_content/<int:int_index>/', views.hdd_order_content, name='hdd_order_content'),
    path('hdd_delete_order/<int:int_index>/', views.hdd_delete_order, name='hdd_delete_order'),
    path('new_hdd_order/', views.hdd_order, name='new_hdd_order'),
    path('new_hdd_orderAlt/', views.hdd_orderAlt, name='new_hdd_orderAlt'),
    path('tar/', views.tar, name='tar'),
    path('tarAlt/', views.tarAlt, name='tarAlt'),
    path('content/<int:int_index>/', views.lot_content, name='lot_content'),
    path('success/', views.success, name='success'),
    # path('content/<int:int_index>/', views.lot_content, name='lot_content'),
    path('', views.index, name='index')
]

on_start()
