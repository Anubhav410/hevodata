from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.services.drive.service import DriveService


class FileSearchView:
    @staticmethod
    def choose_folder(request):
        if request.method == 'GET':
            client_id = request.session['current_client_id']
            return render(request, "choose_folder.html", context={"client_id": client_id})
        else:  # POST
            # save the selected folder-id in session and move them to the Search Text Page
            folder_id = request.POST['folder_id']

            pass  # return render(request, "choose_folder.html", context={"client_id": client_id})

    @api_view(['GET'])
    @staticmethod
    def download_file(request):
        file = DriveService.download_file(request.GET['client_id'], file_id=request.GET['file_id'])
        return Response({"data": file})
