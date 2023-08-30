import logging

from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework.decorators import api_view
from rest_framework.fields import IntegerField, BooleanField, CharField
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.status import HTTP_200_OK

from api.services.drive.service import DriveService

log = logging.getLogger(__name__)


class ChooseFolderSerializer(Serializer):
    folder_id = CharField()
    client_id = CharField()
    setup_watcher = BooleanField(required=False)


class DriveAPIView:
    @staticmethod
    def choose_folder(request):
        log.info("Setting up Folder for sync")
        if request.method == 'GET':
            client_id = request.GET['client_id']
            return render(request, "choose_folder.html", context={"client_id": client_id})
        else:  # POST
            serializer = ChooseFolderSerializer(data=request.POST)
            # save the selected folder-id in session and move them to the Search Text Page
            if serializer.is_valid():
                folder_id = serializer.validated_data['folder_id']
                client_id = serializer.validated_data['client_id']
                setup_watcher = serializer.validated_data.get('setup_watcher', 'False') == 'True'
                DriveService.start_file_injestion(client_id=client_id, folder_id=folder_id, setup_watcher=setup_watcher)
                log.info("Folder Sync Complete")
                return redirect(reverse('search-view') + f"?client_id={client_id}")
        log.info(f"Error with Folder Sync:  {serializer.errors}")
        return render(request, "choose_folder.html")

    @staticmethod
    @api_view(['POST'])
    def watcher_callback(request):
        log.info(f"Google Drive Callback Received, with data: {request.headers}")
        DriveService.update_event_handler(channel_id=request.headers['X-Goog-Channel-Id'])
        return Response(status=HTTP_200_OK)
