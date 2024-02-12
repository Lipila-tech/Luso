from django.urls import path
from . import views
from .views import LoginView, disburse
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

# router.register(r'student', views.StudentView, basename='student')
# router.register(r'parent', views.ParentView, basename='parent')
# router.register(r'payment', views.PaymentView, basename='payment')
# router.register(r'school', views.SchoolView, basename='school')
router.register(r'lipila-payment', views.LipilaCollectionView, basename='lipila-payment')
router.register(r'payment', views.BusinessCollectionView, basename='payment')
router.register(r'user-transactions', views.UserTransactionsView, basename='user-transactions')
router.register(r'products', views.ProductView, basename='products')
router.register(r'signup', views.SignupViewSet, basename='signup')

router.register(r'profile', views.ProfileView, basename='profile')

urlpatterns = [
     path('disburse/', disburse, name='disburse'),
     path('login/', LoginView.as_view(), name='login'),
]

urlpatterns += router.urls