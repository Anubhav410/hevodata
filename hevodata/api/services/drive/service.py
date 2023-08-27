
from api.services.drive.factory import drive_factory


class DriveService:

    @staticmethod
    def download_file(client_id, file_id):
        return drive_factory().get_file_data(client_id=client_id, file_id=file_id)
