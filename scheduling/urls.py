from django.urls import path
from . import views

app_name = 'scheduling'

urlpatterns = [
    # Client URLs (Public)
    path('', views.home, name='home'),
    path('horarios/', views.available_slots, name='available_slots'),
    path('agendar/', views.book_service, name='book_service'),
    path('api/horarios/', views.get_available_slots, name='get_available_slots'),
    path('meus-agendamentos/', views.check_booking, name='check_booking'),
    path('cancelar/', views.cancel_booking, name='cancel_booking'),

    # Admin URLs
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/agendamentos/', views.admin_scheduling_list, name='admin_scheduling_list'),
    path('admin/datas/criar/', views.admin_create_date_slot, name='admin_create_date_slot'),
    path('admin/datas/<int:pk>/', views.admin_date_slot_detail, name='admin_date_slot_detail'),
    path('admin/agendamento-rapido/', views.admin_quick_schedule, name='admin_quick_schedule'),
    path('admin/bloquear/<int:slot_id>/', views.admin_block_time_slot, name='admin_block_time_slot'),
    path('admin/desbloquear/<int:slot_id>/', views.admin_unblock_time_slot, name='admin_unblock_time_slot'),
    path('admin/clientes/', views.admin_client_list, name='admin_client_list'),
    path('admin/clientes/<int:pk>/', views.admin_client_detail, name='admin_client_detail'),

    # API URLs
    path('api/horarios-disponiveis/', views.api_available_slots, name='api_available_slots'),
    path('api/servicos/', views.api_services_by_professional, name='api_services_by_professional'),
]