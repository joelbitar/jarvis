from django.conf.urls import url, patterns
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'.*', TemplateView.as_view(template_name="index.html"), name="index"),
)