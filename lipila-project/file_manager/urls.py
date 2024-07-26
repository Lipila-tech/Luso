from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('upload/', views.media_upload, name='media_upload'),
    path('edit/<str:filename>', views.edit_media_file, name='media_edit'),
    path('play/<str:filename>', views.media_play, name='media_play'),
    path('all/<str:m_type>', views.get_media, name='media_all'),
    path('me/<str:m_type>', views.get_user_media, name='user_media_all'),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)