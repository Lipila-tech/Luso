from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('video/upload', views.video_upload, name='video_upload'),
    path('play/<str:filename>', views.play_video_file, name='play_video'),
    path('play/<str:filename>', views.play_audio_file, name='play_audio'),
    path('audio/upload', views.audio_upload, name='audio_upload'),
    path('all/videos', views.list_video_uploads, name='all_videos'),
    path('all/audios', views.list_audio_uploads, name='all_audios'),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)