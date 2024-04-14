from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
     # Public URLS
     path('', views.index, name='index'),   
        
     # Authenticated User Accounts Urls
     path('accounts/signup/', views.SignupView.as_view(), name='signup'),
          
     # User Logs URLS
     path('transfer-history/', views.log_transfer, name='log_transfer'),
     path('invoice-history/', views.log_invoice, name='log_invoice'),
     # User Logs URLS
    

     path('invoice/', views.invoice, name='invoice'),
     path('transfer/', views.transfer, name='transfer'),
     path('products/history/', views.log_products, name='log_products'),
     path('products/create/', views.CreateProductView.as_view(), name='products'),
     path('products/<int:product_id>/edit/', views.EditProductView.as_view(), name='edit_product'),
     path('products/<int:product_id>/delete/', views.DeleteProductView.as_view(), name='delete_product'),

     # Lipila Admin specific URLS
     path('bnpl/', views.bnpl, name='bnpl'),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)