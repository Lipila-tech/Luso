from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required


urlpatterns = [
     # Public URLS
     path('', views.index, name='index'),
     path('contact', views.contact, name='contact'),
     
     # Accounts URLS
     path('accounts/signup/', views.SignupView.as_view(), name='signup'),
     path('accounts/login/', views.login, name='login'),
     path('accounts/profile/<str:user>', views.profile, name='profile'),
     path('accounts/profile/<str:user>/edit', login_required(views.UpdateUserInfoView.as_view()), name='update_profile'),
     # Authenticated User Accounts Urls
     path('me/<str:user>', views.dashboard, name='dashboard'),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)