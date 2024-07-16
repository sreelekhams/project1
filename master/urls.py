from django.urls import path
from . import views

urlpatterns = [
    path('',views.indexpage,name="indexpage"),
    path('adlogin', views.user_login, name='adlogin'),
    path('admin_logout', views.admin_logout, name='admin_logout'),
    path('department_add', views.department_add, name='department_add'),
    path('department_edit/<str:pk>/', views.department_edit, name='department_edit'),
    path('department_detail/<str:pk>/', views.department_detail, name='department_detail'),
    path('department_list', views.department_list, name='department_list'),
    path('department_delete/<str:pk>/', views.department_delete, name='department_delete'),
    path('designation_add', views.designation_add, name='designation_add'),
     path('designation_edit/<str:pk>/', views.designation_edit, name='designation_edit'),
     path('designation_list', views.designation_list, name='designation_list'),
     path('designation_detail/<str:pk>/', views.designation_detail, name='designation_detail'),
    path('designation_delete/<str:pk>/', views.designation_delete, name='designation_delete'),
    path('location_add', views.location_add, name='location_add'),
    path('location_edit/<str:pk>/', views.location_edit, name='location_edit'),
    path('location_list', views.location_list, name='location_list'),
    path('location_detail/<str:pk>/', views.location_detail, name='location_detail'),
    path('location_delete/<str:pk>/', views.location_delete, name='location_delete'),
    path('employee_add', views.employee_add, name='employee_add'),
    path('designations', views.designations, name='designations'),
    path('employee_list', views.employee_list, name='employee_list'),
    path('employee_edit/<str:pk>/', views.employee_edit, name='employee_edit'),
    path('employee_delete/<str:pk>/', views.employee_delete, name='employee_delete'),
    path('employee_detail/<str:pk>/', views.employee_detail, name='employee_detail'),
    path('user_add', views.user_add, name='user_add'),
    path('user_list', views.user_list, name='user_list'),
     path('user_detail/<str:pk>/', views.user_detail, name='user_detail'),
      path('user_edit/<str:pk>/', views.user_edit, name='user_edit'),
    path('user_delete/<str:pk>/', views.user_delete, name='user_delete'),
    path('employee_report/', views.employee_report, name='employee_report'),
    path('bulk_upload_dep/', views.bulk_upload_dep, name='bulk_upload_dep'),
    path('bulk_upload_des/', views.bulk_upload_des, name='bulk_upload_des'),
    path('bulk_upload_loc/', views.bulk_upload_loc, name='bulk_upload_loc'),
    path('bulk_upload_user/', views.bulk_upload_user, name='bulk_upload_user'),
    path('bulk_upload_emp/', views.bulk_upload_emp, name='bulk_upload_emp'),
    path('export_departments', views.export_departments_to_excel, name='export_departments'),
    path('export_designations', views.export_designations_to_excel, name='export_designations'),
    path('export_locations', views.export_locations_to_excel, name='export_locations'),
    path('export_employees', views.export_employees_to_excel, name='export_employees'),
    path('export_user', views.export_users, name='export_user'),
    path('download_employee_pdf/<str:employee_id>/', views.download_employee_pdf, name='download_employee_pdf'),
    path('send_pdf/', views.send_pdf, name='send_pdf'),
    path('record_audio', views.record_audio, name='record_audio'),
    path('capture_image', views.capture_image, name='capture_image'),
     path('download_selected', views.download_selected, name='download_selected'),
   
   
    
    ]