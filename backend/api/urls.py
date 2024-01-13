from django.urls import path
from . import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

# router.register(r'', views.index, name='index'),
router.register(r'student', views.StudentView, basename='student')
router.register(r'parent', views.ParentView, basename='parent')
router.register(r'payment', views.PaymentView, basename='payment')
router.register(r'school', views.SchoolView, basename='school')
router.register(r'lipila-payment', views.LipilaCollectionView, basename='lipila-payment')

# router.register(r'login', views.LoginView, basename='login')
router.register(r'profile', views.ProfileView, basename='profile')
# router.register(r'logout', views.LogoutView, basename='logout')

urlpatterns = router.urls