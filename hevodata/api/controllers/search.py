import logging

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer

from api.models import Files
from api.services.drive.service import DriveService
from api.services.search.service import SearchService


class FileSerializer(ModelSerializer):
    class Meta:
        model = Files
        fields = ['source_file_id', 'file_name']


log = logging.getLogger(__name__)


class FileSearchView:
    @staticmethod
    @api_view(['GET'])
    def search_view(request):
        if request.method == 'GET':
            client_id = request.GET['client_id']
            return render(request, "search_text.html", context={"client_id": client_id})

    @staticmethod
    @api_view(['POST'])
    def search_api(request):
        search_text = request.POST['search_text']
        client_id = request.POST['client_id']
        response = SearchService.search(client_id=client_id, search_text=search_text)
        return Response({
            "files": FileSerializer(response, many=True).data
        })

    @staticmethod
    @api_view(['GET'])
    def download_file(request):
        file = DriveService.download_file(request.GET['client_id'], file_id=request.GET['file_id'])
        return Response({"data": file})
