from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('video/upload', views.video_upload, name='video_upload'),
    path('audio/upload', views.audio_upload, name='audio_upload'),
    path('all/videos', views.list_video_uploads, name='all_videos'),
    path('all/audios', views.list_audio_uploads, name='all_audios'),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)