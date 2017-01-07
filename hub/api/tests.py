import json

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from django.test.client import RequestFactory

from node.models import Node

from api.vendors.api_ai import ApiAi

from device.models import Device, Room, Placement


# Create your tests here.
class ApiTestsBase(TestCase):
    request_string = """{
                "originalRequest": {
                    "data": {
                        "text": "shipping costs for asia",
                        "match": [
                            "shipping costs for asia"
                        ],
                        "type": "message",
                        "event": "direct_message",
                        "team": "T0FJ03RMP",
                        "user": "U0FLW1N95",
                        "channel": "D4VTEALFP",
                        "ts": "1478131884.000006"
                    },
                    "source": "slack_testbot"
                },
                "id": "0783cd7f-2cf3-482f-b9db-9ab72cc4386b",
                "timestamp": "2017-01-06T08:20:37.459Z",
                "result": {
                    "source": "agent",
                    "resolvedQuery": "turn on lights in the bedroom",
                    "action": "toggle",
                    "actionIncomplete": false,
                    "parameters": {
                        "device_state": "on",
                        "light_type": "all",
                        "location": "bedroom"
                    },
                    "contexts": [],
                    "metadata": {
                        "intentId": "9d6a1b76-3891-44ea-8abc-419b4ba26b71",
                        "webhookUsed": "false",
                        "webhookForSlotFillingUsed": "false",
                        "intentName": "toggle_lights"
                    },
                    "fulfillment": {
                        "speech": "",
                        "messages": [
                            {
                                "type": 0,
                                "speech": ""
                            }
                        ]
                    },
                    "score": 1
                },
                "status": {
                    "code": 200,
                    "errorType": "success"
                },
                "sessionId": "bbadfa67-6f1a-462d-8b24-d9fc986e7f80"
            }"""

    def setUp(self):
        self.api_user = User.objects.create_user(
            username='api_user_test',
            password='test'
        )

        self.client = Client()

        n = Node()
        n.address = 'address'
        n.name = 'Test Node'
        n.api_port = 8001
        n.save()

        d = Device()
        d.name = 'Sovrum taklampa'
        d.slug = 'bedroom_ceiling'
        d.protocol = Device.PROTOCOL_ARCHTEC
        d.model = Device.MODEL_CODESWITCH
        d.node = n
        d.save()

        self.node = n
        self.bedroom_ceiling_light = d

        self.bedroom = Room()
        self.bedroom.name = 'Sovrum'
        self.bedroom.slug = 'bedroom'
        self.bedroom.save()

        self.bedroom_ceiling_light.room = self.bedroom
        self.bedroom_ceiling_light.save()

        self.client.defaults['HTTP_AUTHORIZATION'] = "Token " + str(self.api_user.auth_token.key)

    def refresh(self, obj):
        return obj.__class__.objects.get(pk=obj.pk)


class ApiAiParserTests(ApiTestsBase):
    def setUp(self):
        request_factory = RequestFactory()
        request = request_factory.post(
            reverse('api_entrypoint_api-ai'),
            data=self.request_string
        )

        api_ai = ApiAi(request)

        properties = api_ai.get_properties()

        self.assertEqual(
            properties['action'],
            "toggle"
        )

        self.assertEqual(
            properties['parameters']['device_state'],
            "on"
        )

        self.assertEqual(
            properties['parameters']['light_type'],
            "all"
        )

        self.assertEqual(
            properties['parameters']['location'],
            "bedroom"
        )


class ApiAiAuthenticationTests(ApiTestsBase):
    def test_should_be_able_to_access_site_with_token(self):
        response = self.client.post(
            reverse('api_entrypoint_api-ai'),
            self.request_string,
            content_type='application/json'
        )

        self.assertEqual(
            response.status_code,
            200
        )


class ApiAiTests(ApiTestsBase):
    def test_should_turn_on_devices_in_bedroom_when_sending_bedroom_on(self):
        self.bedroom_ceiling_light.state = 0
        self.bedroom_ceiling_light.save()

        response = self.client.post(
            reverse('api_entrypoint_api-ai'),
            self.request_string,
            content_type='application/json'
        )

        self.assertEqual(
            self.refresh(self.bedroom_ceiling_light).state,
            1
        )
