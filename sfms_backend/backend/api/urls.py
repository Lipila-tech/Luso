from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('login', views.LoginView.as_view()),
	path('payments', views.PaymentView.as_view()),
	path('profile', views.ProfileView.as_view()),
    path('logout', views.LogoutView.as_view()),
    path('history', views.HistoryView.as_view()),
]


