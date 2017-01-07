from django.conf.urls import include, url, patterns

from api.views import EntryPointApiAiView

urlpatterns = patterns('',
    url(r'^api-ai/', EntryPointApiAiView.as_view(), name='api_entrypoint_api-ai'),
)
