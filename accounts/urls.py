from django.urls import path, include
from accounts import views
from api.views import get_swagger_file

urlpatterns = [
    path('signup/', views.signup_view, name="signup"),
    path('sign-out', views.sign_out, name='sign_out'),
    path('signin/', views.custom_login_view, name="signin"),
    path('sent/', views.activation_sent_view, name="activation_sent"),
    path('activate/<str:uidb64>/<str:token>/', views.activate, name="activate"),
    
    #Callback urls
    path('tiktok/callback/', views.tiktok_callback, name='tiktok_callback'),
    path('momo/callback/', views.momo_callback, name='momo_callback'),
    path('google/callback', views.google_callback, name='google_callback'),
    path('tiktok_oauth/', views.tiktok_oauth, name='tiktok_oauth'),

    path('swagger/payments/', get_swagger_file, name='get_swagger_file'),
]
