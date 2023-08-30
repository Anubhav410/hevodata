from rest_framework.serializers import ModelSerializer

from api.models import Files
from api.services.drive.factory import drive_factory
from api.services.search.factory import search_backend_factory


class SearchService:
    @staticmethod
    def search(client_id, search_text):
        # todo: this is not extensible. This needs to support different type of Search BackEnds
        search_back_end = search_backend_factory("postgres")
        return search_back_end.search(client_id=client_id, search_text=search_text)
