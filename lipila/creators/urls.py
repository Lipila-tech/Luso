from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
     # Public URLS
     path('', views.index, name='index'),
     path('<str:user>/contribute', views.contribute, name='contribute'),
     path('<username>/', views.user_profile, name='user_profile'),
      path('accounts/signup/', views.SignupView.as_view(), name='signup'),

      # Authenticated User Accounts Urls
     path('me/<str:user>', views.dashboard, name='creators_dashboard'),
]


if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)