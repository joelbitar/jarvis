import requests

from django.conf import settings

from django.views.generic import View
from django.http import HttpResponse


class RestRouterView(View):
    def get(self, request, path):
        return self.execute_method(request, path, 'get')

    def post(self, request, path):
        return self.execute_method(request, path, 'post')

    def put(self, request, path):
        return self.execute_method(request, path, 'put')

    def delete(self, request, path):
        return self.execute_method(request, path, 'delete')

    def patch(self, request, path):
        return self.execute_method(request, path, 'patch')

    def execute_method(self, request, path, method):
        url = settings.MAIN_HUB_URL + path

        #print('URL', url)


        """
        request_headers = None
        if request.META.get('CONTENT_TYPE', None) is not None:
            request_headers = {}
            request_content_type = request.META.get('CONTENT_TYPE')

            request_headers['content-type'] = request_content_type
        """

        response = getattr(
            requests, method
        ).__call__(
            url,
            data=request.body,
            #headers=request_headers
        )

        r = HttpResponse(
            content=response.content.decode('utf-8'),
            status=response.status_code,
            content_type='application/json',
        )

        return r