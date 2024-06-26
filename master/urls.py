from django.urls import path
from . import views

urlpatterns = [
    path('',views.indexpage,name="indexpage"),
    path('adlogin', views.admin_login, name='adlogin'),
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
    
    ]