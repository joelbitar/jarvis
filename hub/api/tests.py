import json

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from django.test.client import RequestFactory

from node.models import Node

from api.vendors.api_ai import ApiAi
from api.action_router import ActionRouter
from api.actions.toggle import ActionToggle
from api.actions.temperature import GetTemperature

from device.models import Device, Room, Placement, LightType
from sensor.models import Sensor

from api.vendors.api_ai import ApiAiResponse

# Create your tests here.
class ApiTestsBase(TestCase):
    request_string = """{{
                "originalRequest": {{
                    "data": {{
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
                    }},
                    "source": "slack_testbot"
                }},
                "id": "0783cd7f-2cf3-482f-b9db-9ab72cc4386b",
                "timestamp": "2017-01-06T08:20:37.459Z",
                "result": {{
                    "source": "agent",
                    "resolvedQuery": "turn on lights in the bedroom",
                    "action": "{action}",
                    "actionIncomplete": false,
                    "parameters": {parameters},
                    "contexts": [],
                    "metadata": {{
                        "intentId": "9d6a1b76-3891-44ea-8abc-419b4ba26b71",
                        "webhookUsed": "false",
                        "webhookForSlotFillingUsed": "false",
                        "intentName": "toggle_lights"
                    }},
                    "fulfillment": {{
                        "speech": "",
                        "messages": [
                            {{
                                "type": 0,
                                "speech": ""
                            }}
                        ]
                    }},
                    "score": 1
                }},
                "status": {{
                    "code": 200,
                    "errorType": "success"
                }},
                "sessionId": "bbadfa67-6f1a-462d-8b24-d9fc986e7f80"
            }}"""

    def create_device(self, slug, room=None, placement=None, light_type=None, name=None):
        d = Device()
        d.name =  slug or name
        d.slug = slug
        d.protocol = Device.PROTOCOL_ARCHTEC
        d.model = Device.MODEL_CODESWITCH
        d.state = 0
        d.node = self.node
        d.room = room
        d.placement = placement
        d.light_type = light_type
        d.save()

        return d

    def helper_assert_light_has_state(self, *args, state):
        for d in args:
            self.assertEqual(
                self.refresh(d).state,
                state,
                'Device ' + str(d.slug) + ' was not ' + str(state)
            )

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

        self.placements = {}

        self.light_type_ceiling = LightType()
        self.light_type_ceiling.slug = 'ceiling'
        self.light_type_ceiling.name = 'Tak'
        self.light_type_ceiling.save()

        for slug in ['outside', 'inside', 'garden']:
            p = Placement()
            p.slug = slug
            p.save()

            self.placements[slug] = p

        self.node = n

        self.bedroom = Room()
        self.bedroom.name = 'Sovrum'
        self.bedroom.slug = 'bedroom'
        self.bedroom.save()

        self.bathroom = Room.objects.create(
            name="Badrum",
            slug="bathroom"
        )

        self.bedroom_ceiling_light = self.create_device(
            'bedroom_ceiling',
            room=self.bedroom,
            light_type=self.light_type_ceiling
        )

        self.bedroom_ceiling_light.room = self.bedroom
        self.bedroom_ceiling_light.save()

        self.bedroom_window_light = self.create_device(
            'bedroom_window',
            self.bedroom
        )

        self.deck_lights = self.create_device(
            'deck_floor',
            placement=self.placements.get('outside')
        )

        self.client.defaults['HTTP_AUTHORIZATION'] = "Token " + str(self.api_user.auth_token.key)

    def refresh(self, obj):
        return obj.__class__.objects.get(pk=obj.pk)

    def get_api_ai_response(self, **kwargs):
        action = kwargs.get('action', None)

        if action is not None:
            del kwargs['action']

        parameters = json.dumps(kwargs)

        response = self.client.post(
            reverse('api_entrypoint_api-ai'),
            self.request_string.format(
                action=action,
                parameters=parameters
            ),
            content_type='application/json'
        )

        return response


class ApiAiRequestRouterTests(ApiTestsBase):
    def helper_get_action(self, action, parameters=None):
        request_factory = RequestFactory()
        request = request_factory.post(
            reverse('api_entrypoint_api-ai'),
            data=self.request_string.format(
                action=action,
                parameters=json.dumps(
                    parameters or {}
                )
            ),
            content_type="application/json"
        )

        api_ai = ApiAi(request)
        properties = api_ai.get_properties()
        router = ActionRouter()

        return router.get_action(properties)

    def test_should_get_none_action_if_matches_nothing(self):
        action = self.helper_get_action(action="does_not_exist")

        self.assertIsNone(action)

    def test_should_get_toggle_action(self):
        action = self.helper_get_action(action="toggle")

        self.assertIsInstance(
            action,
            ActionToggle
        )

    def test_should_get_get_lights_action(self):
        action = self.helper_get_action(action="get_temperature")

        self.assertIsInstance(
            action,
            GetTemperature
        )


class GetTemperatureActionTests(ApiTestsBase):
    def setUp(self):
        super(GetTemperatureActionTests, self).setUp()

        self.sensor = Sensor.objects.create(
            name="Badrum Temp",
            active=True,
            room=self.bedroom,
            placement=self.placements['inside']
        )
        self.sensor.temperature = 20.0
        self.sensor.save()

        self.living_room_sensor = Sensor.objects.create(
            name="Vardagsrum",
            active=True,
            room=self.bathroom,
            placement=self.placements['inside'],
            temperature=22.0
        )


    def test_get_sensors_in_bedroom(self):
        action = GetTemperature(vendor_name='api_ai')
        sensors = action.get_sensors(
            location_slug=self.bedroom.slug
        )

        self.assertTrue(
            len(sensors) == 1,
            "Should be one sensor"
        )

    def test_get_mean_temperature_from_inside(self):
        action = GetTemperature(vendor_name='api_ai')
        sensors = action.get_sensors(
            location_slug='inside'
        )

        self.assertTrue(
            len(sensors) == 2,
            "Should be two sensors"
        )

        self.assertEqual(
            action.get_temperature(
                sensors=sensors
            ),
            21.0
        )

    def get_temperature_where_there_is_no_sensors(self):
        action = GetTemperature(vendor_name='api_ai')
        sensors = action.get_sensors(
            location_slug='bedroom'
        )

        self.assertTrue(
            len(sensors) == 0,
            "Should be zero sensors"
        )

        self.assertIsNone(
            action.get_temperature(
                sensors=sensors
            )
        )

    def test_get_response_object(self):
        action = GetTemperature(vendor_name='api_ai')

        response = action.run(
            {
                'parameters': {
                    'location': 'inside'
                }
            }
        )

        self.assertIsInstance(
            response,
            ApiAiResponse
        )

        self.assertJSONEqual(
            json.dumps(response.get_dict()),
            json.dumps(
                {
                    "speech": "It is 21.0 degrees",
                    "displayText": "It is 21.0 degrees",
                    "data": {},
                    "contextOut": [],
                    "source": "Yarvis"
                }
            )
        )

    def test_response_to_view_should_be_a_json_response_with_speach(self):
        response = self.get_api_ai_response(
            action="get_temperature",
            location="inside"
        )

        self.assertJSONEqual(
            response.content.decode('utf-8'),
            json.dumps(
                {
                    "speech": "It is 21.0 degrees",
                    "displayText": "It is 21.0 degrees",
                    "data": {},
                    "contextOut": [],
                    "source": "Yarvis"
                }
            )
        )



class ApiAiParserTests(ApiTestsBase):
    def test_api_ai_parser(self):
        request_factory = RequestFactory()
        request = request_factory.post(
            reverse('api_entrypoint_api-ai'),
            data=self.request_string.format(
                action="toggle",
                parameters=json.dumps(
                    {
                        'device_state': "on",
                        'light_type': "all",
                        'location': "bedroom"
                    }
                )
            ),
            content_type="application/json"
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
            self.bedroom.slug
        )


class ApiAiAuthenticationTests(ApiTestsBase):
    def test_should_be_able_to_access_site_with_token(self):
        response = self.get_api_ai_response(
            action="toggle",
            device_state="on",
            light_type="all",
            location=self.bedroom.slug
        )

        self.assertEqual(
            response.status_code,
            200
        )


class ApiAiTests(ApiTestsBase):
    def test_should_turn_on_devices_in_bedroom_when_sending_bedroom_on(self):
        self.bedroom_ceiling_light.state = 0
        self.bedroom_ceiling_light.save()

        response = self.get_api_ai_response(
            action="toggle",
            device_state="on",
            light_type="all",
            location=self.bedroom.slug
        )

        self.assertEqual(
            self.refresh(self.bedroom_ceiling_light).state,
            1
        )

        self.assertEqual(
            self.refresh(self.bedroom_window_light).state,
            1
        )

    def test_should_turn_on_only_bedroom_ceiling_lights(self):
        self.get_api_ai_response(
            action="toggle",
            device_state="on",
            light_type="ceiling",
            location=self.bedroom.slug
        )

        self.assertEqual(
            self.refresh(self.bedroom_ceiling_light).state,
            1,
            "Did NOT turn on ceiling light"
        )

        self.assertEqual(
            self.refresh(self.bedroom_window_light).state,
            0,
            "Whopsie turned on window light"
        )

        self.helper_assert_light_has_state(
            self.bedroom_ceiling_light,
            state=1
        )

        self.helper_assert_light_has_state(
            self.bedroom_window_light,
            state=0
        )

    def test_should_turn_on_devices_that_are_in_outside_placement(self):
        self.get_api_ai_response(
            action="toggle",
            device_state="on",
            light_type="all",
            location=self.placements.get('outside').slug
        )

        self.helper_assert_light_has_state(
            *[d for d in Device.objects.exclude(slug=self.deck_lights.slug)],
            state=0
        )

        self.helper_assert_light_has_state(
            self.deck_lights,
            state=1
        )

    def test_should_be_able_to_turn_on_all_lights(self):
        self.get_api_ai_response(
            action="toggle",
            device_state="on",
            light_type="all",
            location="all"
        )

        self.helper_assert_light_has_state(
            *[d for d in Device.objects.exclude(slug=self.deck_lights.slug)],
            state=1
        )

    def test_should_not_cast_error_when_trying_for_location_that_does_not_exist(self):
        self.get_api_ai_response(
            action="toggle",
            device_state="on",
            light_type="all",
            location="does_not_exist"
        )

        self.helper_assert_light_has_state(
            *[d for d in Device.objects.all()],
            state=0
        )
