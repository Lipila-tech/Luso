from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from patron import views as patron_views

urlpatterns = [
    # lipila public URLS
    path('', views.index, name='index'),
    path('contact', views.contact, name='contact'),

    # PatronUser defined authenticated user views
    path('me/<str:user>', patron_views.dashboard, name='dashboard'),
    path('me/staff/<str:user>', views.staff_users, name='staff_dashboard'),
        
    # lipila difened authenticated user views
    path('approve_withdrawals/', views.approve_withdrawals, name ='approve_withdrawals'),
    path('processed_withdrawals/', views.processed_withdrawals, name ='processed_withdrawals'),
    path('faq/', views.pages_faq, name='faq'),
    path('terms-of-use/', views.pages_terms, name='terms'),
    path('privacy-policy/', views.pages_privacy, name='privacy'),

    # Modal-forms urls
    path('withdrawals/request', views.CreateWithdrawalRequest.as_view(), name ='withdrawals'),
    path('update/<int:pk>', views.TierUpdateView.as_view(), name ='update_tier'),
    path('view/<int:pk>', views.TierReadView.as_view(), name ='view_tier'),
    path('delete/<int:pk>', views.TierDeleteView.as_view(), name ='delete_tier'),

    path('payments/sendmoney/<str:type>/<int:id>', views.SendMoneyView.as_view(), name='send_money_id'),
    path('payments/sendmoney/', views.SendMoneyView.as_view(), name='send_money_transfer'),
    path('unsubscribe/<int:tier_id>', views.UnsubScribeView.as_view(), name='unsubscribe'),
    path('tiers/', views.tiers, name = 'tiers'),

    path('approve/<int:pk>', views.ApproveWithdrawModalView.as_view(), name='approve_withdraw'),
    path('reject/<int:pk>', views.RejectWithdrawModalView.as_view(), name='reject_withdraw'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
