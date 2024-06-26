from django.urls import path
from . import views

urlpatterns = [
    path('indexpage',views.indexpage,name="indexpage"),
    path('', views.admin_login, name='adlogin'),
    path('department_add', views.department_add, name='department_add'),
    path('department_edit/<str:pk>/', views.department_edit, name='department_edit'),
    path('department_list', views.department_list, name='department_list'),
    path('department_delete/<str:pk>/', views.department_delete, name='department_delete'),
    path('designation_add', views.designation_add, name='designation_add'),
     path('designation_edit/<str:pk>/', views.designation_edit, name='designation_edit'),
     path('designation_list', views.designation_list, name='designation_list'),
    path('designation_delete/<str:pk>/', views.designation_delete, name='designation_delete'),
    path('location_add', views.location_add, name='location_add'),
    path('location_edit/<str:pk>/', views.location_edit, name='location_edit'),
    path('location_list', views.location_list, name='location_list'),
    path('location_delete/<str:pk>/', views.location_delete, name='location_delete'),
    
    ]