import requests
import json

from django.utils import timezone
from django.core import mail

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from node.models import Node

from node.serializers import NodeSerializer


class NodeViewSet(viewsets.ModelViewSet):
    queryset = Node.objects.all()
    serializer_class = NodeSerializer 


class NodeCommandViewBase(APIView):
    def execute_request(self, node):
        raise NotImplementedError()

    def build_url(self, node, command):
        return '{node_url}/conf/{command}/'.format(
                node_url=node.address,
                command=command
            )

    def is_in_test_mode(self):
        return hasattr(mail, 'outbox')


    def get(self, request, pk):
        node = Node.objects.get(pk=pk)

        return self.execute_request(node)

class NodeWriteConfView(NodeCommandViewBase):
    def execute_request(self, node):
        if self.is_in_test_mode():
            return Response()

        response = requests.post(
            self.build_url(node, 'write'),
        )

        return Response()

class NodeRestartDaemonView(NodeCommandViewBase):
    def execute_request(self, node):
        response = requests.post(
            self.build_url(node, 'restart-daemon'),
        )

        return Response()


