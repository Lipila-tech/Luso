from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
     # Public URLS
     path('', views.index, name='index'),   
                  
     # User Logs URLS
     path('transfer-history/', views.log_transfer, name='log_transfer'),

     path('transfer/', views.transfer, name='transfer'),
    
     # Student actions urls
     path('student/all', views.list_student, name='list_student'),
     path('student/create', views.CreateStudentView.as_view(), name='students'),
     path('student/<int:student_id>/edit/', views.EditStudentView.as_view(), name='edit_student'),
     path('student/<int:student_id>/delete/', views.DeleteStudentView.as_view(), name='delete_student'),
     # Product action urls
     path('product/all', views.log_products, name='log_products'),
     path('product/create', views.CreateProductView.as_view(), name='products'),
     path('product/<int:product_id>/edit/', views.EditProductView.as_view(), name='edit_product'),
     path('product/<int:product_id>/delete/', views.DeleteProductView.as_view(), name='delete_product'),

     # Lipila Admin specific URLS
     path('bnpl/', views.bnpl, name='bnpl'),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)