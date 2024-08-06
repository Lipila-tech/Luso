"""
backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/

Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.index, name='index')
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='index')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# Uncomment next two lines to enable admin:
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404

urlpatterns = [
    # adminstrations urls
    path('admin/', admin.site.urls),

    # api urls
    path('', include('lipila.urls')),
    path('patron/', include(('patron.urls', 'patron'), namespace='patron')),
    path('api/v1/', include('api.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('multimedia/', include(('file_manager.urls', 'file_manager'), namespace='file_manager')),
]