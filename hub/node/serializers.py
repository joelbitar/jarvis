from rest_framework import serializers
from node.models import Node


class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node 


class NodeDetailsSerializer(NodeSerializer):
    pass