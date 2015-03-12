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

        response = getattr(
            requests, method
        ).__call__(
            url,
            data=request.body,
            headers=request_headers
        )

        r = HttpResponse(
            content=response.content.decode('utf-8'),
            status=response.status_code,
            content_type='application/json',
        )

        return r