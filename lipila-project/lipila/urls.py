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
    path('accounts/profile/', patron_views.profile, name='profile'),
    path('accounts/profile/choose', patron_views.choose_profile_type,
         name='choose_profile_type'),
    path('accounts/profile/create/creator', patron_views.create_creator_profile,
         name='create_creator_profile'),
    path('accounts/profile/create/patron', patron_views.create_patron_profile,
         name='create_patron_profile'),
    path('accounts/profile/edit/<str:user>',
         patron_views.EditUserProfile.as_view(), name='update_profile'),
    path('me/<str:user>', patron_views.dashboard, name='dashboard'),
    path('patron/all/', patron_views.patron, name='patron'),
    path('patron/join/<str:user>/<str:creator>/', patron_views.join, name='join'),

    # lipila difened authenticated user views
    path('withdraw/<str:user>', views.withdraw, name='withdraw'),
    path('history/<str:user>', views.history, name='history'),
    path('faq/', views.pages_faq, name='faq'),
    path('terms-of-use/', views.pages_terms, name='terms'),
    path('privacy-policy/', views.pages_privacy, name='privacy'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
