__author__ = 'joel'

from django.conf.urls import patterns, url
from django.views.decorators.csrf import csrf_exempt

from git_hook.views import GitHookView

urlpatterns = patterns('',
    url(r'^hook/$', csrf_exempt(GitHookView.as_view()) , name='git_hook'),
)
