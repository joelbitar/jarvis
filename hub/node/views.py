from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from node.models import Node

from node.serializers import NodeSerializer

from node.communicator import NodeCommunicator


class NodeViewSet(viewsets.ModelViewSet):
    queryset = Node.objects.all()
    serializer_class = NodeSerializer 


class NodeCommandViewBase(APIView):
    def execute_request(self, node):
        raise NotImplementedError()

    def get(self, request, pk):
        node = Node.objects.get(pk=pk)

        if not self.execute_request(node):
            return Response(status=500)

        return Response()


class NodeWriteConfView(NodeCommandViewBase):
    def execute_request(self, node):
        communicator = NodeCommunicator(node=node)
        return communicator.write_conf()

class NodeRestartDaemonView(NodeCommandViewBase):
    def execute_request(self, node):
        communicator = NodeCommunicator(node=node)
        return communicator.restart_daemon()


