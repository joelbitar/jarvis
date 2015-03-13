from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from node.models import Node
from node.serializers import NodeSerializer
from node.communicator import NodeCommunicator


class NodeViewSet(viewsets.ModelViewSet):
    queryset = Node.objects.all()
    serializer_class = NodeSerializer 


class NodeCommandViewBase(APIView):
    permission_classes = (IsAdminUser, )

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
        if communicator.write_conf():
            return Response()

class NodeRestartDaemonView(NodeCommandViewBase):
    def execute_request(self, node):
        communicator = NodeCommunicator(node=node)
        if communicator.restart_daemon():
            return Response()


class NodeSyncView(NodeCommandViewBase):
    def execute_request(self, node):
        for device in node.device_set.filter(node_device_pk=None):
            device.get_communicator().create()

        return True