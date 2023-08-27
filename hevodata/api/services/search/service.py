from rest_framework.serializers import ModelSerializer

from api.models import Files
from api.services.drive.factory import drive_factory


class SearchService:
    @staticmethod
    def start_file_injestion(client_id, folder_id):
        drive = drive_factory()
        files = drive.get_files(client_id=client_id, folder_id=folder_id)

        for file in files:
            content = drive.get_file_data(client_id=client_id, file_id=file['id'])
            stored_file = Files.objects.update_or_create(
                source_file_id=file["id"], client_id=client_id,
                defaults={"file_name": file['name'], "source": "google", "source_file_id": file['id'],
                          "mime_type": file['mimeType'], "file_content": content})

    @staticmethod
    def search(client_id, search_text):
        return Files.objects.raw(
            f"select id, file_name, source_file_id from api_files where client_id='{client_id}' and ts @@ phraseto_tsquery('english', '{search_text}')")
