from django.shortcuts import render
from django.core import mail
from django.conf import settings
import json
import subprocess

from rest_framework.views import APIView
from rest_framework.response import Response


# These views work differently than the ones in hub git_hook
# Create your views here.
class GitHookView(APIView):
    def is_in_test_mode(self):
        if hasattr(mail, 'outbox'):
            return True
        else:
            return False

    def post(self, request):
        if self.is_in_test_mode():
            print("is in test mode, does NOT execute script :", settings.GITHUB_WEBHOOK_EXECUTE_PATH)
        else:
            subprocess.call([settings.GITHUB_WEBHOOK_EXECUTE_PATH])

        return Response({})
