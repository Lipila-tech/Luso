from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

# router.register(r'payments/mtn', views.MtnCollectionView, basename='payments')
router.register(r'disburse', views.MtnDisbursementView, basename='disburse')


# Add a path for browsing the API
urlpatterns = [
    path('login/', views.APILoginView.as_view(), name='api-login'),
    path('airtel/request-payment/', views.AirtelPaymentRequestView.as_view(), name='airtel-request-payment'),
    path('mtn/request-payment/', views.MTNPaymentRequestView.as_view(), name='mtn-request-payment'),
    path('mtn/callback/', views.MtnPaymentCallbackView.as_view(), name='mtn-callback'),
    path('airtel/callback/', views.AirtelPaymentCallbackView.as_view(), name='airtel-callback'),

    # Include the router's registered URLs
    path('', include(router.urls)),
    
    # include DRF's default browser view for API endpoints
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
