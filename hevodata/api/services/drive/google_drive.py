import json
import random

import requests
from django.conf import settings
from googleapiclient.errors import HttpError

from api.models import Channels
from api.services.drive.base import BaseDrive
from api.services.oauth.service import OAuthService


class GoogleDrive(BaseDrive):
    def setup_watcher(self, client_id, folder_id):
        creds = OAuthService.get_credentials(client_id=client_id)
        try:
            api_url = f"https://www.googleapis.com/drive/v3/files/{folder_id}/watch"
            auth_token = creds.token

            # Create headers with the authentication token
            headers = {
                "Authorization": f"Bearer {auth_token}",
                "Content-Type": "application/json"
            }

            data = {
                "type": "web_hook",
                "address": settings.WATCHER_URL,
                "id": random.Random().randint(1, 100000),
            }

            # Make a GET request to the API with the headers
            response = requests.post(api_url, data=json.dumps(data), headers=headers)
            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Print the response content (JSON or text)
                channel = response.json()
                Channels.objects.create(client_id=client_id, channel_id=channel['id'], file_id=folder_id)
            else:
                print(f"Request failed with status code: {response.status_code}")
        except HttpError as error:
            print(F'An error occurred: {error}')

    def get_files(self, client_id, folder_id):
        files = []
        creds = OAuthService.get_credentials(client_id=client_id)
        try:
            api_url = f"https://www.googleapis.com/drive/v3/files?q='{folder_id}' in parents"
            auth_token = creds.token

            # Create headers with the authentication token
            headers = {
                "Authorization": f"Bearer {auth_token}"
            }

            # Make a GET request to the API with the headers
            response = requests.get(api_url, headers=headers)
            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Print the response content (JSON or text)
                files = response.json()['files']
            else:
                print(f"Request failed with status code: {response.status_code}")
        except HttpError as error:
            print(F'An error occurred: {error}')

        return files

    def get_file_contents(self, client_id, file_id):
        creds = OAuthService.get_credentials(client_id=client_id)
        try:
            api_url = f"https://www.googleapis.com/drive/v3/files/{file_id}?alt=media"
            auth_token = creds.token

            # Create headers with the authentication token
            headers = {
                "Authorization": f"Bearer {auth_token}"
            }

            # Make a GET request to the API with the headers
            response = requests.get(api_url, headers=headers)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Print the response content (JSON or text)
                return response.content
            else:
                print(f"Request failed with status code: {response.status_code}")
        except HttpError as error:
            print(F'An error occurred: {error}')

        return None

    def get_file_info(self, client_id, file_id):
        creds = OAuthService.get_credentials(client_id=client_id)
        try:
            api_url = f"https://www.googleapis.com/drive/v3/files/{file_id}"
            auth_token = creds.token
            # Create headers with the authentication token
            headers = {
                "Authorization": f"Bearer {auth_token}"
            }

            # Make a GET request to the API with the headers
            response = requests.get(api_url, headers=headers)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Print the response content (JSON or text)
                return response.json()
            else:
                print(f"Request failed with status code: {response.status_code}")
        except HttpError as error:
            print(F'An error occurred: {error}')

        return response.content

    def handle_channel_updates(self, channel_id):
        channel = Channels.objects.get(channel_id=channel_id)
        # creds = OAuthService.get_credentials(client_id=channel.client_id)
        self.get_files(client_id=channel.client_id, folder_id=channel.file_id)

    def get_latest_change_changes(self, creds, file_id):
        try:
            api_url = f"https://www.googleapis.com/drive/v3/files/{file_id}/changes"
            auth_token = creds.token
            # Create headers with the authentication token
            headers = {
                "Authorization": f"Bearer {auth_token}"
            }
            # Make a GET request to the API with the headers
            response = requests.get(api_url, headers=headers)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Print the response content (JSON or text)
                json_data = response.json()
                if 'largestChangeId' in json_data:
                    api_url = f"https://www.googleapis.com/drive/v3/files/{file_id}/changes/{json_data['largestChangeId']}"
                    response = requests.get(api_url, headers=headers)
        except:
            return None
