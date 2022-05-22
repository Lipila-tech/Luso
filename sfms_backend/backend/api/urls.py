from django.urls import path
#from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
	path('login', views.LoginView.as_view()),
	path('payments', views.PaymentView.as_view()),
	path('profile', views.ProfileView.as_view()),
    path('logout', views.LogoutView.as_view()),
    #path('request', views.request_to_pay_view, name='request'),
]

#urlpatterns = format_suffix_patterns(urlpatterns)
