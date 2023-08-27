from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from api.services.drive.service import DriveService


class DriveAPIView:
    @staticmethod
    def choose_folder(request):
        if request.method == 'GET':
            client_id = request.GET['client_id']
            return render(request, "choose_folder.html", context={"client_id": client_id})
        else:  # POST
            # save the selected folder-id in session and move them to the Search Text Page
            folder_id = request.POST['folder_id']
            client_id = request.POST['client_id']
            DriveService.start_file_injestion(client_id=client_id, folder_id=folder_id, setup_watcher=True)
            return redirect(reverse('search-view') + f"?client_id={client_id}")

    @staticmethod
    @api_view(['POST'])
    def watcher_callback(request):
        return Response(status=HTTP_200_OK)

        DriveService.update_event_handler(channel_id=request.headers['X-Goog-Channel-Id'])
        return Response(status=HTTP_200_OK)
