__author__ = 'joel'

from django.conf.urls import patterns, url

from git_hook.views import GitHookView

urlpatterns = patterns('',
    url(r'^hook/$', GitHookView.as_view(), name='git_hook'),
)
