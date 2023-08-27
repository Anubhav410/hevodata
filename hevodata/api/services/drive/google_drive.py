import requests
from googleapiclient.errors import HttpError

from api.services.drive.base import BaseDrive
from api.services.oauth.service import OAuthService


class GoogleDrive(BaseDrive):
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

    def get_file_data(self, client_id, file_id):
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
                print(response.content)
            else:
                print(f"Request failed with status code: {response.status_code}")
        except HttpError as error:
            print(F'An error occurred: {error}')

        return response.content
