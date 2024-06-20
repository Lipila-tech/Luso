from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register(r'payments', views.LipilaCollectionView, basename='payments')
router.register(r'disburse', views.LipilaDisbursementView, basename='disburse')

urlpatterns = [
    path('login/', views.APILoginView.as_view(), name='api-login'),
]

urlpatterns += router.urls
