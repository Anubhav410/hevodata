from django.urls import path

from .controllers.choose_folder import FileSearchView
from .controllers.oauth import OAuthAPIView

urlpatterns = [
    path('oauth/initiate', OAuthAPIView.initiate_oauth),
    path('oauth/callback', OAuthAPIView.callback_handler),
    path('files/download', FileSearchView.download_file),

]
