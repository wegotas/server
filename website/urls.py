from django.urls import path
from . import views
from django.views.generic import TemplateView


urlpatterns = [
    path('edit/<int:int_index>/', views.edit, name='edit'),
    path('edit/<int:int_index>/print_qr/', views.print_computer_qr, name='print_computer_qr'),
    path('edit/<int:int_index>/print_qr/<slug:printer>/', views.print_computer_qr_with_printer, name='print_computer_qr_with_printer'),
    path('remove_ramstick_from_computer/<int:ramstick_id>/<int:computer_id>/', views.remove_ramstick_from_computer, name='remove_ramstick_from_computer'),
    path('remove_drive_from_computer/<int:drive_id>/<int:computer_id>/', views.remove_drive_from_computer, name='remove_drive_from_computer'),
    path('observations_to_add/<int:int_index>/<keyword>/', views.observations_to_add, name='observations_to_add'),
    path('assign_observation_to_computer/<int:observation_id>/<int:computer_id>/', views.assign_observation_to_computer, name='assign_observation_to_computer'),
    path('remove_observation_from_computer/<int:observation_id>/<int:computer_id>/', views.remove_observation_from_computer, name='remove_observation_from_computer'),
    path('get_observation/<int:observation_id>/', views.get_observation, name='get_observation'),
    path('remove_battery_from_computer/<int:battery_id>/<int:computer_id>/', views.remove_battery_from_computer, name='remove_battery_from_computer'),

    path('ramsticks_to_add/<int:int_index>/<keyword>/', views.ramsticks_to_add, name='ramsticks_to_add'),
    path('get_ramstick/<int:ramstick_id>/', views.get_ramstick, name='get_ramstick'),
    path('add_nonexistant_ramstick/<int:computer_id>/', views.add_nonexistant_ramstick, name='add_nonexistant_ramstick'),

    path('processors_to_add/<int:int_index>/<keyword>/', views.processors_to_add, name='processors_to_add'),
    path('get_processor/<int:processor_id>/', views.get_processor, name='get_processor'),

    path('gpus_to_add/<int:int_index>/<keyword>/', views.gpus_to_add, name='gpus_to_add'),
    path('get_gpu/<int:gpu_id>/', views.get_gpu, name='get_gpu'),

    path('delete_charger_cat/<int:int_index>/', views.delete_charger_category, name='delete_charger_category'),
    path('by_serial/<slug:serial>/', views.edit_by_serial, name='edit_by_serial'),
    path('serial/<slug:serial>/', views.serial_processing, name='serial_processing'),
    path('serial/<slug:serial>/delete/', views.delete_charger_from_scan, name='delete_charger'),
    path('edit_charger/<int:int_index>/edit/', views.edit_charger_serial, name='edit_charger_edit'),
    path('edit_charger/<int:int_index>/print/', views.print_charger_serial, name='print_charger'),
    path('edit_charger/<int:int_index>/print_serials/', views.print_chargers_serials, name='print_chargers_serials'),
    path('edit_charger/<int:int_index>/delete/', views.delete_charger, name='delete_charger'),
    path('edit_charger/<int:int_index>/', views.edit_charger, name='edit_charger'),

    path('delete_order/<int:int_index>/', views.delete_order, name='delete_order'),
    path('edit_order/<int:int_index>/', views.edit_order, name='edit_order'),
    path('strip_order/<int:int_index>/', views.strip_order, name='strip_order'),
    path('computer_search_table_from_order/', views.computer_search_table_from_order, name='computer_search_table_from_order'),
    path('edit_order/<int:order_id>/add_computer/', views.add_computer_to_order, name='add_computer_to_order'),
    path('edit_order/<int:int_index>/excel/', views.order_excel, name='order_excel'),
    path('edit_order/<int:int_index>/csv/', views.order_csv, name='order_csv'),

    path('received_batch/<int:int_index>/', views.received_batch_content_view, name='received_batch_content'),
    path('received_batch_excel/<int:int_index>/', views.received_batch_excel_view, name='received_batch_excel_view'),
    path('received_batch_csv/<int:int_index>/', views.received_batch_csv_view, name='received_batch_csv_view'),

    path('mass_delete/', views.mass_delete, name='mass_delete'),
    path('mass_excel/', views.mass_excel, name='mass_excel'),
    path('mass_csv/', views.mass_csv, name='mass_csv'),
    path('mass_qr_print/', views.mass_qr_print, name='mass_qr_print'),
    path('mass_qr_print/<slug:printer>/', views.mass_qr_print_with_printer, name='mass_qr_print_with_printer'),
    path('mass_change_box/<int:int_index>/', views.mass_change_box, name='mass_change_box'),

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

    path('received_batches/del/<int:int_index>/', views.delreceivedBatch, name='delelete_batch'),
    path('received_batches/edit/', views.recieved_batch_edit, name='batch_edit'),
    path('received_batches/', views.receivedbatches, name='batches'),

    path('computer_form_factors/', views.computer_form_factors, name='computer_form_factors'),
    path('computer_form_factors/del/<int:int_index>/', views.del_computer_form_factor, name='delelete_computer_form_factor'),
    path('computer_form_factors/edit/', views.computer_form_factor_edit, name='computer_form_factor_edit'),

    path('observ/', views.observations, name='observations'),
    path('observ/cat/del/<int:int_index>/', views.del_observation_category, name='observationCategoryDeletion'),
    path('observ/cat/edit/', views.observation_category_edit, name='observationCategoryEdit'),
    path('observ/cat/', views.observation_category, name='observationCategory'),

    path('observ/sub/del/<int:int_index>/', views.del_observation_subcategory, name='observationCategoryDeletion'),
    path('observ/sub/edit/', views.observation_subcategory_edit, name='observationCategoryEdit'),
    path('observ/sub/', views.observation_subcategory, name='observationSubcategory'),

    path('observ/details/del/<int:int_index>/', views.delete_observations_details, name='delete_observations_details'),
    path('observ/details/edit/', views.edit_observations_details, name='edit_observations_details'),
    path('observ/details/', views.observations_details, name='observationsDetails'),

    path('cat_to_sold/', views.cat_to_sold, name='cat_to_sold'),
    path('hdd_edit/<int:int_index>/', views.hdd_edit, name='hdd_edit'),
    path('hdd_delete/<int:int_index>/', views.hdd_delete, name='hdd_delete'),
    path('view_pdf/<int:int_index>/', views.view_pdf, name='view_pdf'),
    path('hdd_order_content/<int:int_index>/', views.drive_order_content, name='drive_order_content'),
    path('hdd_order_content/<int:int_index>/csv/', views.drive_order_content_csv, name='drive_order_content_csv'),
    path('hdd_delete_order/<int:int_index>/', views.drive_delete_order, name='drive_delete_order'),

    path('new_drive_order/', views.drive_order_view, name='drive_order'),

    path('tar/', views.process_tar_view, name='tar'),

    path('content/<int:int_index>/', views.lot_content, name='lot_content'),
    path('success/', views.success, name='success'),
    path('', views.index_view, name='index'),

    path('drives/', views.drives_view, name='drives'),
    path('lots/', views.lots_view, name='lots'),
    path('drive_orders/', views.drive_orders_view, name='drive_orders'),
    path('chargers/', views.chargers_view, name='chargers'),
    path('orders/', views.orders_view, name='orders'),
    path('sold/', views.sold_view, name='sold'),
    path('received_batches_list/', views.received_batches_list, name='received_batches_list'),
    path('boxes/', views.boxes_view, name='boxes'),
    path('typcat/', views.typcat_view, name='typcat'),
    path('search/', views.search_view, name='search'),
    path('export/', views.export_view, name='export'),
]
