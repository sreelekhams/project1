from django.urls import path
from . import views

urlpatterns = [
    path('indexpage',views.indexpage,name="indexpage"),
    path('', views.admin_login, name='adlogin'),
    path('department_add', views.department_add, name='department_add'),
    path('department_edit/<str:pk>/', views.department_edit, name='department_edit'),
    path('department_list', views.department_list, name='department_list'),
    path('department_delete/<str:pk>/', views.department_delete, name='department_delete'),
    
    
    ]