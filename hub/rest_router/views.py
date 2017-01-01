import json

import requests

from django.conf import settings

from django.views.generic import View
from django.http import HttpResponse


class RestRouterView(View):
    def get(self, request, path):
        return self.execute_method(request, path, 'get')

    def post(self, request, path):
        print('PO_ST')
        return self.execute_method(request, path, 'post')

    def put(self, request, path):
        return self.execute_method(request, path, 'put')

    def delete(self, request, path):
        return self.execute_method(request, path, 'delete')

    def patch(self, request, path):
        return self.execute_method(request, path, 'patch')

    def execute_method(self, request, path, method):
        url = settings.MAIN_HUB_URL + path

        request_headers = {}

        # Map from To, if no second entry in set, just copy.
        header_properties_map = (
            ('HTTP_X_CSRFTOKEN',),
            ('CONTENT_TYPE', 'content-type'),
            ('COOKIE', 'cookie'),
            ('HTTP_AUTHORIZATION', 'Authorization',),
        )

        for header_property_name in header_properties_map:
            requests_header_key = header_property_name[0]
            request_meta_key = requests_header_key

            if len(header_property_name) == 2:
                requests_header_key = header_property_name[1]

            request_headers[requests_header_key] = request.META.get(request_meta_key)

        response_status_code = 500
        response_content = {}
        response_content_type = 'application/json'

        try:
            # Get the method form 'requests' lib and execute it
            response = getattr(
                requests, method
            ).__call__(
                url,
                data=request.body,
                headers=request_headers
            )

            response_content = response.content.decode('utf-8')
            response_status_code = response.status_code
            if hasattr(response.headers, 'Content-Type'):
                response_content_type = response.headers['Content-Type']
        except requests.ConnectionError:
            # If there was a connection-error, communicate this.
            response_status_code = 502
            response_content = json.dumps({
                'error': 'connection-error',
                'message': 'Could not connect to main hub',
            })

        return HttpResponse(
            content=response_content,
            status=response_status_code,
            content_type=response_content_type,
        )
