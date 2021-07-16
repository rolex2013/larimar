"""larimar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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

from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('', include('accounts.urls')),
    #path('main/', include('main.urls')),
    path('', include('main.urls')),
    path('companies/', include('companies.urls')),
    path('projects/', include('projects.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('accounts/', include('accounts.urls')),
    path('finance/', include('finance.urls')),
    path('crm/', include('crm.urls')),
    path('docs/', include('docs.urls')),
    path('files/', include('files.urls')),
    path('feedback/', include('feedback.urls')),
    #path('media/', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),    
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]

# без этого ckeditor не видит загруженные на сервер файлы/картинки (https://qarchive.ru/37247_django_media_url_i_media_root)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
