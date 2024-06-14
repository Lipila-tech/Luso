from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from business.views import CreateProductView, EditProductView, DeleteProductView

urlpatterns = [
     # Public URLS
     path('', views.index, name='index'),
     path('contribute/<str:creator>', views.contribute, name='contribute'),

     path('creators/list', views.list_creators, name='creators'),
     path('payments/pay/<int:tier_id>', views.make_payment, name='make_payment'),
     path('home/<str:creator>/', views.creator_home, name='creator_home'),
     path('my-tiers', views.view_tiers, name='tiers'),
     path('my-tiers/edit/<int:tier_id>', views.edit_tiers, name='edit_tier'),
     path('join/<int:tier_id>', views.join, name='join_tier'),
     path('unsubscribe/<int:tier_id>', views.unsubscribe_patron, name='unsubscribe'),
     path('patron/all/', views.patron, name='patrons'),
     path('payments/history/', views.payments_history, name='payments'),
     path('subscriptions/', views.subscriptions, name='subscriptions'),
     path('subscription/<int:tier_id>', views.subscription_detail, name='subscription_detail'),
]


if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)