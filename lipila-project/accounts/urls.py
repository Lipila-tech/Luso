from django.urls import path, include
from accounts import views

urlpatterns = [
    path('signup/', views.signup_view, name="signup"),
    path('sign-out', views.sign_out, name='sign_out'),
    path('signin/', views.custom_login_view, name="signin"),
    path('sent/', views.activation_sent_view, name="activation_sent"),
    path('activate/<str:uidb64>/<str:token>/', views.activate, name="activate"),
    path('auth-receiver/', views.auth_receiver, name='auth_receiver'),
]
