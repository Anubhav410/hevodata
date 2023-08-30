from api.models import Files


class BaseSearchBackEnd:
    def search(self, client_id, search_text):
        print("implement this function")


class PostgresSearchBackend(BaseSearchBackEnd):
    def search(self, client_id, search_text):
        return Files.objects.raw(
            f"select id, file_name, source_file_id from api_files where client_id='{client_id}' and ts @@ phraseto_tsquery('english', '{search_text}')")
