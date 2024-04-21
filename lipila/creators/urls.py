from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from business.views import CreateProductView, EditProductView, DeleteProductView

urlpatterns = [
     # Public URLS
     path('', views.index, name='index'),
     path('<str:user>/contribute', views.contribute, name='contribute'),
     path('accounts/signup/', views.SignupView.as_view(), name='signup'),

     path('patrons', views.list_patrons, name='patrons'),
#      path('product/all', CreateProductView.as_view(), name='products'),
#      path('product/<int:product_id>/edit/', EditProductView.as_view(), name='edit_product'),
#      path('product/<int:product_id>/delete/', DeleteProductView.as_view(), name='delete_product'),
]


if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)