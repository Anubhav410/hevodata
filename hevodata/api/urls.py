from django.urls import path

from .controllers.drive import DriveAPIView
from .controllers.oauth import OAuthAPIView
from .controllers.search import FileSearchView

urlpatterns = [
    path('oauth/initiate', OAuthAPIView.initiate_oauth),
    path('oauth/callback', OAuthAPIView.callback_handler),
    path('files/download', FileSearchView.download_file),
    path('search', FileSearchView.search_api, name='search-api'),
    path('drive/watcher', DriveAPIView.watcher_callback, name='drive-watcher'),

]
