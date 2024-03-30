from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register(r'payments', views.LipilaCollectionView, basename='payments')
router.register(r'signup', views.SignupViewSet, basename='signup')


urlpatterns = [
    path('login/', views.LoginView.as_view(), name='api-login'),
]

urlpatterns += router.urls
