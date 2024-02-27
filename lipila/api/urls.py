from django.urls import path
from . import views
from .views import LoginView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register(r'payments', views.LipilaCollectionView, basename='payments')
router.register(r'products', views.ProductView, basename='products')
router.register(r'signup', views.SignupViewSet, basename='signup')

router.register(r'profile', views.ProfileView, basename='profile')

urlpatterns = [
     path('login/', LoginView.as_view(), name='login'),
]

urlpatterns += router.urls

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL,
#                           document_root=settings.MEDIA_ROOT)

# handler404 = 