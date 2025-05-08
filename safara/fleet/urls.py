from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Driver URLs
    path('drivers/', views.driver_list, name='driver_list'),
    path('drivers/<int:pk>/', views.driver_detail, name='driver_detail'),
    path('drivers/create/', views.driver_create, name='driver_create'),
    path('drivers/<int:pk>/update/', views.driver_update, name='driver_update'),
    path('drivers/<int:pk>/delete/', views.driver_delete, name='driver_delete'),
    
    # Vehicle URLs
    path('vehicles/', views.vehicle_list, name='vehicle_list'),
    path('vehicles/<int:pk>/', views.vehicle_detail, name='vehicle_detail'),
    path('vehicles/create/', views.vehicle_create, name='vehicle_create'),
    path('vehicles/<int:pk>/update/', views.vehicle_update, name='vehicle_update'),
    path('vehicles/<int:pk>/delete/', views.vehicle_delete, name='vehicle_delete'),
    
    # Driver Assignment URLs
    path('assign-driver/', views.assign_driver, name='assign_driver'),
    path('unassign-driver/<int:assignment_id>/', views.unassign_driver, name='unassign_driver'),
    
    # Fuel Log URLs
    path('fuel-logs/', views.fuel_log_list, name='fuel_log_list'),
    path('fuel-logs/create/', views.fuel_log_create, name='fuel_log_create'),
    path('fuel-logs/<int:pk>/update/', views.fuel_log_update, name='fuel_log_update'),
    path('fuel-logs/<int:pk>/delete/', views.fuel_log_delete, name='fuel_log_delete'),
    
    # Tonnage Log URLs
    path('tonnage-logs/', views.tonnage_log_list, name='tonnage_log_list'),
    path('tonnage-logs/create/', views.tonnage_log_create, name='tonnage_log_create'),
    path('tonnage-logs/<int:pk>/update/', views.tonnage_log_update, name='tonnage_log_update'),
    path('tonnage-logs/<int:pk>/delete/', views.tonnage_log_delete, name='tonnage_log_delete'),
]