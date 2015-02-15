from django.db import models


class Node(models.Model):
    name = models.CharField(max_length=56)
    address = models.CharField(max_length=128)
