from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.views.generic import RedirectView

from main.views import pageNotFound

from django.views.i18n import JavaScriptCatalog

# from django.conf.urls.i18n import i18n_patterns #добавляем в адреса языковый префикс

# urlpatterns = i18n_patterns()
urlpatterns = [
    path('favicon.ico/', RedirectView.as_view(url='/static/image/favicon.ico')),
    path('admin/', admin.site.urls),
    path('rosetta/', include('rosetta.urls')),
    # path('', include('accounts.urls')),
    # path('main/', include('main.urls')),
    path('', include('main.urls')),
    path('companies/', include('companies.urls')),
    path('projects/', include('projects.urls')),
    # path('ckeditor/', include('ckeditor_uploader.urls')),
    path("ckeditor5/", include("django_ckeditor_5.urls")),    
    path('accounts/', include('accounts.urls')),
    path('finance/', include('finance.urls')),
    path('crm/', include('crm.urls')),
    path('docs/', include('docs.urls')),
    path('files/', include('files.urls')),
    path('feedback/', include('feedback.urls')),
    path('chats/', include('chats.urls')),
    path('lists/', include('lists.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('jscat/', JavaScriptCatalog.as_view(), name='js-catalog'),
    # path('media/', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),    
]

if settings.DEBUG:
    import debug_toolbar
    # urlpatterns += [
    #     path('__debug__/', include(debug_toolbar.urls)),
    urlpatterns = [path("__debug__/", include("debug_toolbar.urls"))] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)        
    # ]

# без этого ckeditor не видит загруженные на сервер файлы/картинки (https://qarchive.ru/37247_django_media_url_i_media_root)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# if settings.DEBUG:
#     urlpatterns = [path("__debug__/", include("debug_toolbar.urls"))] + urlpatterns
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# handler500 = serverError
handler400 = pageNotFound
# handler403 = accessDenided
# handler404 = badRequest

# TODO не забыть про возможность перенаправления на другие страницы (redirect)
