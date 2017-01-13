from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication

from api.vendors.api_ai import ApiAi
from api.action_router import ActionRouter


"""
Entry point for api.ai
"""
class EntryPointApiAiView(APIView):

    def post(self, request):
        api_ai = ApiAi(request)

        properties = api_ai.get_properties()

        router = ActionRouter()
        router.set_vendor_name(vendor_name='api_ai')
        result = router.execute(properties)

        return Response(result.get_dict())
