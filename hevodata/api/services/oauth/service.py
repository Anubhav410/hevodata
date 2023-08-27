import datetime
from datetime import timedelta

import google_auth_oauthlib.flow
import requests
from django.conf import settings
from django.utils import timezone

from api.models import GoogleCredentials


class OAuthService:
    @staticmethod
    def get_credentials(client_id):
        credentials = GoogleCredentials.objects.get(client_id=client_id)
        if credentials.expiry < timezone.now():
            # need to refresh the token
            credentials = OAuthService.refresh_token(credentials=credentials)
        return credentials

    @staticmethod
    def refresh_token(credentials):
        api_url = f"https://accounts.google.com/o/oauth2/token?grant_type=refresh_token&refresh_token={credentials.refresh_token}&client_id={credentials.client_id}&client_secret={credentials.client_secret}"

        # Create headers with the authentication token

        # Make a GET request to the API with the headers
        response = requests.post(api_url)
        if response.status_code == 200:
            response = response.json()
            credentials.token = response['access_token']
            credentials.expiry = timezone.now() + timedelta(seconds=response['expires_in'])
            credentials.save()
        else:
            print(f"Request failed with status code: {response.status_code}")
        return credentials

    @staticmethod
    def get_oauth_initiate_url():
        flow = google_auth_oauthlib.flow.Flow.from_client_config(
            settings.GOOGLE_CONFIG,
            scopes=settings.GOOGLE_REQUESTED_SCOPES)
        flow.redirect_uri = settings.GOOGLE_REDIRECT_URI
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true')

        return authorization_url, state

    @staticmethod
    def callback_handler(state, code, scope):
        flow = google_auth_oauthlib.flow.Flow.from_client_config(
            settings.GOOGLE_CONFIG,
            scopes=settings.GOOGLE_REQUESTED_SCOPES,
            state=state)
        flow.redirect_uri = settings.GOOGLE_REDIRECT_URI
        flow.fetch_token(code=code)

        credentials = flow.credentials

        # adding to database
        google_credentials, is_created = GoogleCredentials.objects.update_or_create(
            client_id=credentials.client_id,
            defaults={
                "token": credentials.token,
                "refresh_token": credentials.refresh_token,
                "token_uri": credentials.token_uri,
                "client_secret": credentials.client_secret,
                "scopes": credentials.scopes,
                "expiry": credentials.expiry}
        )
        return google_credentials
