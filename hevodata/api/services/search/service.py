from rest_framework.serializers import ModelSerializer

from api.models import Files
from api.services.drive.factory import drive_factory


class SearchService:
    @staticmethod
    def search(client_id, search_text):
        return Files.objects.raw(
            f"select id, file_name, source_file_id from api_files where client_id='{client_id}' and ts @@ phraseto_tsquery('english', '{search_text}')")
