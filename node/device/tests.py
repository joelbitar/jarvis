from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from device.models import Device
from device.conf import DeviceConfig
from device.conf import TellstickConfig
from django.conf import settings
import json

from device.models import DeviceCommand

from device.message.command import DeviceCommandMessage


class BasicDeviceTest(TestCase):
    def setUp(self):
        self.device = Device(
            name='Test device',
            protocol='arctech',
            model='codeswitch',
            house="A",
            unit="1",
        )
        self.device.save()

        self.user = User.objects.create_user(
            username='test',
            password='test'
        )

        client = Client()
        client.login(
            username='test',
            password='test'
        )

        self.maxDiff = 5000
        self.logged_in_client = client


class DeviceConfigTests(BasicDeviceTest):
    def test_render_template_from_device(self):
        device_conf_object = DeviceConfig(device=self.device)

        self.assertNotEqual("", device_conf_object.render_device_conf())

        self.assertIsInstance(device_conf_object.render_device_conf(), str)

    def test_render_through_config_renderer_and_through_the_device_shortcut_is_the_same(self):
        device_conf_object = DeviceConfig(device=self.device)

        self.assertEqual(
            device_conf_object.render_device_conf(),
            self.device.render_config()
        )


class TellstickConfigTests(BasicDeviceTest):
    def test_render_tellstick_config_is_a_string(self):
        tc = TellstickConfig(
            devices=Device.objects.all()
        )

        self.assertNotEqual("", tc.render_config())
        self.assertIsNotNone(tc.render_config())

        self.assertIsInstance(tc.render_config(), str)


class TellstickTestSwitchCommands(BasicDeviceTest):
    def test_call_turn_on_device(self):
        self.device.commands.turn_on()

    def test_call_turn_off_device(self):
        self.device.commands.turn_off()

    def test_learn_device(self):
        self.device.commands.learn()


class TestCaseWithLoggedInClient(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test',
            password='test'
        )

        client = Client()
        client.login(
            username='test',
            password='test'
        )

        self.logged_in_client = client


class DevicesListCall(TestCaseWithLoggedInClient):
    def setUp(self):
        super(DevicesListCall, self).setUp()

        for i in range(10):
            d = Device(
                name="Device {i}".format(i=i),
                protocol='arctech',
                model='codeswitch',
                house="A",
                unit="1",
            )
            d.save()

        self.maxDiff = 5000

    def test_get_device_list_should_get_all_devices(self):
        response = self.logged_in_client.get(
            reverse('device-list')
        )

        j = json.loads(response.content.decode('utf-8'))

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertEqual(
            len(j),
            10
        )


class DeviceRestCreateDevice(TestCaseWithLoggedInClient):
    def test_create_device_should_return_device_info(self):
        response = self.logged_in_client.post(
            '/devices/',
            {
                'name': 'testDevice',
                'model': 'model',
                'protocol': 'protocol',
            }
        )

        self.assertEqual(
            response.status_code,
            201
        )

        self.assertEqual(
            Device.objects.all()[0].pk,
            json.loads(response.content.decode('utf-8'))['id']
        )


class DeviceRestCrud(BasicDeviceTest):
    def setUp(self):
        super(DeviceRestCrud, self).setUp()
        self.client = self.logged_in_client

    def test_delete_device_should_remove_device(self):
        self.client.delete(
            '/devices/{pk}/'.format(pk=self.device.pk)
        )

        self.assertEqual(
            0,
            Device.objects.all().count()
        )

    def test_update_device_should_change_device_properties(self):
        response = self.client.put(
           '/devices/{pk}/'.format(pk=self.device.pk),
            json.dumps({
                'name': 'UPDATED',
                'model': 'updated',
                'protocol': 'updated'
            }),
            content_type='application/json'
        )

        self.assertEqual(
            response.status_code,
            200,
            response.content
        )

        device = Device.objects.get(pk=self.device.pk)

        self.assertEqual(
            device.name,
            'UPDATED'
        )

        self.assertEqual(
            device.model,
            'updated'
        )


    def test_get_details_should_return_device_information(self):
        response = self.client.get(
            '/devices/{pk}/'.format(pk=self.device.pk),
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertJSONEqual(
            response.content.decode('utf-8'),
            json.dumps(
                {
                    'id': self.device.pk,
                    'name': self.device.name,
                    'model': self.device.model,
                    'protocol' : self.device.protocol,
                    'code': self.device.code,
                    'controller': self.device.controller,
                    'description' : self.device.description,
                    'devices': self.device.devices,
                    'house': self.device.house,
                    'unit': self.device.unit,
                    'system': self.device.system,
                    'units': self.device.units,
                    'fade': self.device.fade,
                    'written_to_conf': self.device.written_to_conf,
                }
            )
        )


class DeviceCommandTests(BasicDeviceTest):
    def test_should_set_excuted_after_execution(self):
        self.device.written_to_conf = True
        self.device.save()

        url = reverse('device-command', kwargs={'pk' : self.device.pk})

        response = self.logged_in_client.post(
            url,
            {
                'command' : 'on'
            }
        )

        dc = DeviceCommand.objects.get(pk=1)
        self.assertIsNone(
            dc.executed
        )

        dc.execute()

        dc = DeviceCommand.objects.get(pk=dc.pk)

        self.assertIsNotNone(
            dc.executed
        )


class DeviceRestNotWritten(BasicDeviceTest):
    def setUp(self):
        super(DeviceRestNotWritten, self).setUp()
        self.device.written_to_conf = False
        self.device.save()

    def test_should_return_conflict_if_not_written(self):
        url = reverse('device-command', kwargs={'pk' : self.device.pk})

        for command_name in ['on', 'off', 'learn']:
            response = self.logged_in_client.post(
                url,
                {
                    'command': command_name
                }
            )

            self.assertEqual(
                response.status_code,
                409
            )

        self.assertEqual(
            0,
            DeviceCommand.objects.all().count()
        )


class DeviceRestCallTests(BasicDeviceTest):
    def setUp(self):
        super(DeviceRestCallTests, self).setUp()
        self.device.written_to_conf = True
        self.device.save()

    def test_send_on_command(self):
        url = reverse('device-command', kwargs={'pk' : self.device.pk})

        response = self.logged_in_client.post(
            url,
            {
                'command' : 'on'
            }
        )

        self.assertEqual(response.status_code, 201)

        self.assertEqual(
            DeviceCommand.objects.all().count(),
            1
        )

        dc = DeviceCommand.objects.all()[0]

        self.assertEqual(
            dc.command_name,
            'on'
        )

        self.assertIsNotNone(
            dc.command_data_json
        )
        self.assertEqual(
            dc.command_data_json,
            '{}'
        )

        self.assertEqual(
            dc.command_data,
            {}
        )

    def test_should_receive_a_ok_when_sending_dim_command(self):
        url = reverse('device-command', kwargs={'pk' : self.device.pk})

        response = self.logged_in_client.post(
            url,
            json.dumps({
                'command': 'dim',
                'data': {
                    'dimlevel' : 50
                }
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 201)

        self.assertEqual(
            DeviceCommand.objects.all().count(),
            1
        )

        dc = DeviceCommand.objects.all()[0]

        self.assertEqual(
            dc.command_name,
            'dim'
        )

        self.assertIsNotNone(
            dc.command_data_json
        )

        self.assertJSONEqual(
            dc.command_data_json,
            json.dumps(
                {
                    'dimlevel' : 50,
                }
            )
        )

        self.assertEqual(
            dc.command_data,
            {
                'dimlevel' : 50
            }
        )


    def test_should_not_be_able_to_send_command_that_does_not_exist(self):
        url = reverse('device-command', kwargs={'pk' : self.device.pk})

        response = self.logged_in_client.post(
            url,
            {
                'command' : 'asdf'
            }
        )

        self.assertEqual(response.status_code, 400)

        response = self.logged_in_client.post(
            url,
            {
                'not_spelled_correctly' : 'on'
            }
        )

        self.assertEqual(response.status_code, 400)

    def test_should_receive_a_not_found_if_the_id_of_a_device_does_not_exist(self):
        url = reverse('device-command', kwargs={'pk' : 666})

        response = self.logged_in_client.post(
            url,
            {
                'command' : 'on'
            }
        )

        self.assertEqual(response.status_code, 404)


class DeviceRestTests(BasicDeviceTest):
    def test_should_be_able_to_update_a_device(self):
        response = self.logged_in_client.put(
                '/devices/' + str(self.device.pk) + '/',
                json.dumps({
                    'name' : 'New name',
                    'model' : 'model',
                    'protocol' : 'protocol',
                }),
                content_type='application/json'
            )

        self.assertEqual(response.status_code, 200, response.content)


class WriteConfigRESTTest(BasicDeviceTest):
    def test_should_respond_with_ok_when_trying_to_write_conf(self):
        self.assertEqual(1, Device.objects.filter(written_to_conf=False).count())

        response = self.logged_in_client.post(
                '/conf/write/', {}
            )

        self.assertEqual(response.status_code, 200, response.content)

        self.assertEqual(0, Device.objects.filter(written_to_conf=False).count())


class RestartTelldusRESTTest(BasicDeviceTest):
    def test_should_respond_with_ok_when_trying_restart_daemon(self):
        response = self.logged_in_client.post(
                '/conf/restart-daemon/', {}
            )

        self.assertEqual(response.status_code, 200, response.content)


class DeviceCommandMessageDecodeTests(BasicDeviceTest):
    def test_should_be_able_to_decode_json_and_have_properties_of_command(self):
        msg = '{"device_id": 1, "command_name": "test", "command_data" : {}}'

        devcommsg = DeviceCommandMessage(msg)

        devcommsg.decode()

        self.assertEqual(
            devcommsg.device.pk,
            self.device.pk
        )

        self.assertEqual(
            devcommsg.command_name,
            "test"
        )

    def test_if_command_data_is_empty_should_be_a_empty_dict(self):
        msg = '{"device_id": 1, "command_name": "test"}'

        devcommsg = DeviceCommandMessage(msg)

        devcommsg.decode()

        self.assertEqual(
            devcommsg.command_data,
            {}
        )

    def test_should_be_able_to_execute_command(self):
        msg = '{"device_id": 1, "command_name": "on"}'
        devcommsg = DeviceCommandMessage(msg)
        devcommsg.decode()

        self.assertTrue(
            devcommsg.execute()
        )


class DeviceCommandMessageEncodeTests(BasicDeviceTest):
    def test_should_encode_basic_data(self):
        dcm = DeviceCommandMessage()
        dcm.device = self.device
        dcm.command_name = 'on'

        dcm.encode()

        self.assertJSONEqual(
            dcm.message_string,
            json.dumps(
                {
                    'device_id': self.device.pk,
                    'command_name': 'on',
                    'command_data': {}
                }
            )
        )

    def test_should_be_able_to_set_arbitrary_command_data(self):
        dcm = DeviceCommandMessage()
        dcm.device = self.device
        dcm.command_name = 'dim'
        dcm.set_command_data('dimlevel', 50)
        dcm.encode()

        self.assertJSONEqual(
            dcm.message_string,
            json.dumps(
                {
                    'device_id': self.device.pk,
                    'command_name': 'dim',
                    'command_data': {
                        'dimlevel': 50
                    }
                }
            )
        )




