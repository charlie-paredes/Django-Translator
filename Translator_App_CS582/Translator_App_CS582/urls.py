"""
URL configuration for Translator_App_CS582 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from translator import views  # Import views from your app
from django.urls import re_path
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),  # Map the root URL to your view
    path(
        #"translation_result/<str:translated_text>/",
        "translation_result/<str:translated_text>/<path:translated_audio>/",
        views.translation_result,
        name="translation_result",
    ),
    path("translate/", views.translate, name="translate"),  # Add this line
    
    re_path(r'^audio/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    }),
    
]