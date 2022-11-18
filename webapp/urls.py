from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('docs/', docs, name='docs'),
    path('shablon/', temp, name='temp'),
    path('reports/', reports, name='reports'),
    path('data/', data, name='data'),
    path('groups/', groups, name='groups'),
    path('users/', users, name='users'),
    path('api-keys/', api_keys, name='api-keys'),
    path('download_file/', download_file, name='download_file'),
    path('export_file/', export_file, name='export_file'),
    path('delete_file/', delete_file, name='delete_file'),
    path('create_file/',create_file,name='create_file')
]