from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from business.views import CreateProductView, EditProductView, DeleteProductView

urlpatterns = [
     # Public URLS
     path('', views.index, name='index'),
     path('<str:user>/contribute', views.contribute, name='contribute'),

     path('creators/list', views.list_creators, name='creators'),
     path('home/<str:creator>/', views.creator_home, name='creator_home'),
     path('my-tiers', views.view_tiers, name='tiers'),
     path('my-tiers/edit/<int:tier_id>', views.edit_tiers, name='edit_tier'),
     path('join/<int:tier_id>', views.join, name='join_tier'),
     path('patron/all/', views.patron, name='patrons'),
]


if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)