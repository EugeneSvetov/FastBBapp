from django.urls import path

from fastbbot_webapp import settings
from .views import *
from django.conf.urls.static import static

from .views import _export_file, _download_file, _delete_file, _delete_package, _create_file, _api_keys

urlpatterns = [
    path('', home, name='home'),
    path('shablon/', temp, name='temp'),
    path('reports/', reports, name='reports'),
    path('data/', data, name='data'),
    path('groups/', groups, name='groups'),
    path('users/', users, name='users'),
    path('api-keys/', _api_keys, name='api-keys'),
    path('exports/', exports, name='exports'),
    path('download_file/<str:down>/<str:id>/<str:name>', _download_file, name='download_file'),
    path('export_file/<str:down>/<str:id>/<str:name>', _export_file, name='export_file'),
    path('delete_file/<str:down>/<str:id>/<str:name>', _delete_file, name='delete_file'),
    path('delete_package/<str:down>/<str:id>/<str:name>', _delete_package, name='delete_package'),
    path('create_file/<str:down>',_create_file,name='create_file')
]

if settings.DEBUG: # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)