from django.urls import path
from django.contrib.auth import views as auth_views
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

    # Admin Login/Logout
    path('gestao/login/', auth_views.LoginView.as_view(template_name='scheduling/admin/login.html'), name='admin_login'),
    path('gestao/logout/', auth_views.LogoutView.as_view(next_page='/'), name='admin_logout'),

    # Admin Dashboard URLs (Protected)
    path('gestao/', views.admin_dashboard, name='admin_dashboard'),
    path('gestao/agendamentos/', views.admin_scheduling_list, name='admin_scheduling_list'),
    path('gestao/datas/criar/', views.admin_create_date_slot, name='admin_create_date_slot'),
    path('gestao/datas/<int:pk>/', views.admin_date_slot_detail, name='admin_date_slot_detail'),
    path('gestao/agendamento-rapido/', views.admin_quick_schedule, name='admin_quick_schedule'),
    path('gestao/bloquear/<int:slot_id>/', views.admin_block_time_slot, name='admin_block_time_slot'),
    path('gestao/desbloquear/<int:slot_id>/', views.admin_unblock_time_slot, name='admin_unblock_time_slot'),
    path('gestao/clientes/', views.admin_client_list, name='admin_client_list'),
    path('gestao/clientes/<int:pk>/', views.admin_client_detail, name='admin_client_detail'),

    # API URLs
    path('api/horarios-disponiveis/', views.api_available_slots, name='api_available_slots'),
    path('api/servicos/', views.api_services_by_professional, name='api_services_by_professional'),
]