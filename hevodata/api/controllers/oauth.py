from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from api.services.oauth.service import OAuthService


class OAuthAPIView:
    @staticmethod
    @api_view(['GET'])
    def initiate_oauth(request):
        return Response({
            "url": OAuthService.get_oauth_initiate_url()
        })

    @staticmethod
    @api_view(['GET'])
    def callback_handler(request):
        state = request.GET.get("state", None)
        code = request.GET.get("code", None)
        scope = request.GET.get("scope", None)

        google_credentials = OAuthService.callback_handler(state=state, code=code, scope=scope)
        request.session['current_client_id'] = google_credentials.client_id
        return redirect("choose-folder")
