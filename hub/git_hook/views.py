from django.shortcuts import render
from django.core import mail
from django.conf import settings
import json
import subprocess

import hmac
from hashlib import sha1

import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from node.models import Node
from node.communicator import NodeCommunicator


class GitHubSecretAuthentication(BaseAuthentication):
    def get_hub_signature_from_header(self, request):
        possible_headers = (
            'X-Hub-Signature',
            'HTTP_X_HUB_SIGNATURE',
        )
        for header_key in possible_headers:
            header_value = request.META.get(header_key, None)

            if header_value is not None:
                return str(header_value)

        raise AuthenticationFailed('Could not find signature')

    def calculate_github_sha_signature(self, request, secret=None):
        secret = secret or settings.GITHUB_WEBHOOK_SECRET

        # HMAC requires the key to be bytes, but data is string
        mac = hmac.new(bytearray(secret, encoding='utf-8'), msg=request.body, digestmod=sha1)

        return "sha1=" + str(mac.hexdigest())

    def authenticate(self, request):
        #print('Signatures', self.get_hub_signature_from_header(request), self.calculate_github_sha_signature(request))
        if self.get_hub_signature_from_header(request) == self.calculate_github_sha_signature(request):
            return (None, None)

        raise AuthenticationFailed('Signature did not match')

# Create your views here.
class GitHookView(APIView):
    permission_classes = ()
    authentication_classes = (GitHubSecretAuthentication,)

    def is_in_test_mode(self):
        if hasattr(mail, 'outbox'):
            return True
        else:
            return False

    def execute_requests_to_nodes(self):
        # run upgrade_node(). on node communicator
        result = []

        for node in Node.objects.all():
            node_communicator = NodeCommunicator(node=node)

            result.append(
                {
                    "node": {
                        "name": node.name,
                        "address": node.address
                    },
                    "success": node_communicator.upgrade_node(),
                }
            )

        return result

    def execute_request_to_main_hub(self):
        if settings.MAIN_HUB_URL is None:
            return None

        if self.is_in_test_mode() or settings.MAIN_HUB_URL.startswith("http://example.com"):
            print('Is In test mode, doest NOT execute request to ' + settings.MAIN_HUB_URL + 'githook/hook/')
            return False

        try:
            response = requests.post(
                settings.MAIN_HUB_URL + 'githook/hook/',
                headers={
                    'X-Hub-Signature': settings.GITHUB_WEBHOOK_SECRET
                }
            )
        except requests.ConnectionError:
            return {
                "success": False,
                "error": "connection_refused"
            }

        return {
            "success": response.status_code in [202, 200],
            "status_code": response.status_code
        }

    def post(self, request):
        try:
            payload = json.loads(request.body.decode('utf-8'))
        except Exception:
            print('No payload', dir(request))
            print(request.content_type)
            print(request.body)
            return Response(status=500)

        # Check that we are at master branch
        if payload.get('ref') is None or not payload.get('ref').endswith("master"):
            return Response("Was not for master", status=400)

        # If in test mode do not call to subprocess
        if self.is_in_test_mode():
            print("is in test mode, does NOT execute script :", settings.GITHUB_WEBHOOK_EXECUTE_PATH)
        else:
            subprocess.call([settings.GITHUB_WEBHOOK_EXECUTE_PATH])

        return Response(
            {
                "main_hub" : self.execute_request_to_main_hub(),
                "nodes": self.execute_requests_to_nodes(),
                "test_mode": self.is_in_test_mode()
            },
            status=202
        )
