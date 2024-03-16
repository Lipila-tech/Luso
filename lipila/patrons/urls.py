from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
     # Public URLS
     path('', views.index, name='index'),
     path('<str:user>/contribute', views.contribute, name='contribute'),
     
]


if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)