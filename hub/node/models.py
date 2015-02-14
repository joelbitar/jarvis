from django.db import models

class Node(models.Model):
    name = models.CharField(max_length=56)
    ip = models.GenericIPAddressField()
    hostname = models.CharField(max_length=12)
