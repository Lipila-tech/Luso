from django.urls import path
from . import views


urlpatterns = [
     path('', views.index, name='index'),
     path('payment/', views.send_money, name='payment'),
     path('service-details/', views.service_details, name='service-details'),
     path('portfolio-details/', views.portfolio_details, name='portfolio-details'),
     path('disburse/', views.disburse, name='disburse'),

     # authenticated user endpoints
     path('dashboard/<int:id>', views.dashboard, name='dashboard'),
     path('users-profile/<int:id>', views.users_profile, name='users-profile'),
     path('pages-faq/', views.pages_faq, name='pages-faq'),


]