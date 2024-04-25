from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required


urlpatterns = [
     # Public URLS
     path('', views.index, name='index'),
     path('creators/all/', views.creators, name='creators'),
     path('creators/join/<str:user>/<str:creator>/', views.join, name='join'),
     path('contact', views.contact, name='contact'),
     
     # Accounts URLS
     path('accounts/signup/', views.SignupView.as_view(), name='signup'),
     path('accounts/login/', views.login, name='login'),
     path('accounts/profile/<str:user>', views.profile, name='profile'),
     path('accounts/profile/<str:user>/edit', login_required(views.UpdateUserInfoView.as_view()), name='update_profile'),
     # Authenticated User Accounts Urls
     path('me/<str:user>', views.dashboard, name='dashboard'),
     path('withdraw/<str:user>', views.withdraw, name='withdraw'),
     path('history/<str:user>', views.history, name='history'),
     path('faq/', views.pages_faq, name='faq'),
     path('terms-of-use/', views.pages_terms, name='terms'),
     path('privacy-policy/', views.pages_privacy, name='privacy'),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)