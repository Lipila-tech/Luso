from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from business.views import CreateProductView, EditProductView, DeleteProductView

urlpatterns = [
     # Public URLS
     path('', views.index, name='index'),
     path('payments/contribute/<int:tier_id>', views.contribute, name='contribute'),
     path('payments/pay/<int:tier_id>', views.make_payment, name='make_payment'),

     path('creators/list', views.list_creators, name='creators'),
     path('payments/status/', views.check_payment_status, name='check_payment_status'),
     path('home/<str:creator>/', views.creator_home, name='creator_home'),
     path('my-tiers', views.view_tiers, name='tiers'),
     path('my-tiers/edit/<int:tier_id>', views.edit_tiers, name='edit_tier'),
     path('join/<int:tier_id>', views.join, name='join_tier'),
     path('unsubscribe/<int:tier_id>', views.unsubscribe_patron, name='unsubscribe'),
     path('patron/all/', views.patron, name='patrons'),
     path('subscriptions/', views.subscriptions, name='subscriptions'),
     path('subscription/<int:tier_id>', views.subscription_detail, name='subscription_detail'),
     path('withdraw/', views.creator_withdrawal, name='withdraw'),

     # Profile views
     path('accounts/profile/', views.profile, name='profile'),
     path('accounts/profile/edit/<str:user>/patron', views.EditPatronProfile.as_view(), name='update_profile'),
     path('accounts/profile/edit/<str:user>', views.EditPersonalInfo.as_view(), name='update_personal_info'),
     path('accounts/profile/choose', views.choose_profile_type,
         name='choose_profile_type'),
     path('accounts/profile/create/creator', views.create_creator_profile,
          name='create_creator_profile'),
     path('accounts/profile/create/patron', views.create_patron_profile,
          name='create_patron_profile'),

     # Authenticated User's Transaction History endpoints
     path('history/withdrawals/', views.withdrawal_history, name='withdrawals_history'),
     path('history/pay/', views.payments_history, name='subscriptions_history'),
     path('history/contribute/', views.contributions_history, name='contributions_history'),
]


if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)