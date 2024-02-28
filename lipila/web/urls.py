from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
     # Public URLS
     path('', views.index, name='index'),
     path('payment/', views.send_money, name='payment'),
     path('service-details/', views.service_details, name='service-details'),
     path('portfolio-details/', views.portfolio_details, name='portfolio-details'),
     path('pages-faq/', views.pages_faq, name='pages-faq'),     
     path('signup/', views.signup, name='signup'),
     path('login/', views.login, name='login'),
     
     # Authenticated User Urls
     path('dashboard/<int:id>', views.dashboard, name='dashboard'),
     path('users-profile/<int:id>', views.users_profile, name='users-profile'),
     path('disburse/', views.disburse, name='disburse'),
     path('logout/', views.logout, name='logout'),
     path('history/', views.history, name='history'),
     path('bnpl/', views.bnpl, name='bnpl'),
     path('sales/', views.sales, name='sales'),
]


if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)