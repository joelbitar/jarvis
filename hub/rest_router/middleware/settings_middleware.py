from django.conf import settings


class SettingsMiddleware(object):
    def process_template_response(self, request, response):
        # Add settings stuff to template

        if response.context_data:
            response.context_data['MAIN_PROXY_URL'] = settings.MAIN_HUB_URL

        return response

