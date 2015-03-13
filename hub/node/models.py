from django.db import models


class Node(models.Model):
    name = models.CharField(max_length=56)
    address = models.CharField(max_length=128)
    auth_token = models.CharField(max_length=40, null=True, default=None)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'node'


class RequestLog(models.Model):
    url = models.CharField(max_length=256)
    method = models.CharField(max_length=12)
    request_data = models.TextField(blank=True, null=True, default=None)

    response_status_code = models.PositiveSmallIntegerField(null=True,blank=True,default=None)
    response_data = models.TextField(blank=True, null=True, default=None)

    # Timestamp
    request_sent = models.DateTimeField(auto_now_add=True)
    response_received = models.DateTimeField(null=True, default=None, blank=True)

    class Meta:
        app_label = 'node'
