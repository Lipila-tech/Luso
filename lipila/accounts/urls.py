from django.urls import path, include
from accounts import views

urlpatterns = [
    path('signup/', views.signup_view, name="signup"),
    path('login/', views.login_view, name="login"),
    path('sent/', views.activation_sent_view, name="activation_sent"),
    path('activate/<str:uidb64>/<str:token>/', views.activate, name="activate"),
    path('accounts/', include('django.contrib.auth.urls')),
]
