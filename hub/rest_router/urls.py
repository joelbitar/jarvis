__author__ = 'joel'

from django.conf.urls import patterns, url

from rest_router.views import RestRouterView

urlpatterns = patterns('',
    url(r'(?P<path>.*)?', RestRouterView.as_view(), name='hub-proxy'),
    #url(r'(?P<path>[^\?]*)?', RestRouterView.as_view(), name='hub-proxy'),
)
