from django.conf import settings

from django.core.urlresolvers import reverse


class SettingsMiddleware(object):
    def process_template_response(self, request, response):
        # Add settings stuff to template

        if response.context_data:
            response.context_data['USE_PROXY'] = settings.MAIN_HUB_URL is not None
            response.context_data['PROXY_URL'] = reverse('hub-proxy').lstrip('/')

        return response

