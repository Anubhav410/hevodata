from api.models import Files, Channels
from api.services.drive.factory import drive_factory
from api.services.oauth.service import OAuthService


class DriveService:
    @staticmethod
    def start_file_injestion(client_id, folder_id, setup_watcher=True):
        drive = drive_factory()
        files = drive.get_files(client_id=client_id, folder_id=folder_id)
        if setup_watcher:
            drive.setup_watcher(client_id=client_id, folder_id=folder_id)

        for file in files:
            file_info = drive.get_file_info(client_id=client_id, file_id=file['id'])
            if 'labels' in file_info and 'trashed' in file_info['labels'] and file_info['labels']['trashed']:
                Files.objects.filter(client_id=client_id, source_file_id=file_info['id']).delete()
                continue

            content = drive.get_file_contents(client_id=client_id, file_id=file['id'])
            stored_file = Files.objects.update_or_create(
                source_file_id=file["id"], client_id=client_id,
                defaults={"file_name": file['name'], "source": "google", "source_file_id": file['id'],
                          "mime_type": file['mimeType'], "file_content": content})

    @staticmethod
    def download_file(client_id, file_id):
        # return drive_factory().get_file_data(client_id=client_id, file_id=file_id)
        return drive_factory().get_files(client_id=client_id, folder_id=file_id)

    @staticmethod
    def update_event_handler(channel_id):
        channel = Channels.objects.get(channel_id=channel_id)
        DriveService.start_file_injestion(client_id=channel.client_id, folder_id=channel.file_id, setup_watcher=False)
        # drive_factory().handle_channel_updates(channel_id)
