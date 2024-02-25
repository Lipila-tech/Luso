from django.urls import path
from . import views
from .views import LoginView, disburse
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse


router = DefaultRouter()

router.register(r'payments', views.LipilaCollectionView, basename='payments')
router.register(r'user-transactions', views.UserTransactionsView, basename='user-transactions')
router.register(r'products', views.ProductView, basename='products')
router.register(r'signup', views.SignupViewSet, basename='signup')

router.register(r'profile', views.ProfileView, basename='profile')

urlpatterns = [
     path('index/', views.index, name='index'),
     path('service-details/', views.service_details, name='service-details'),
     path('portfolio-details/', views.portfolio_details, name='portfolio-details'),
     path('disburse/', disburse, name='disburse'),
     path('login/', LoginView.as_view(), name='login'),

     # authenticated user endpoints
     path('dashboard/<int:id>', views.dashboard, name='dashboard'),
     path('users-profile/<int:id>', views.users_profile, name='users-profile'),
     path('pages-faq/', views.pages_faq, name='pages-faq'),


]

urlpatterns += router.urls

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL,
#                           document_root=settings.MEDIA_ROOT)

# handler404 = 