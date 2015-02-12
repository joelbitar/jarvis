from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from device.models import Device
from device.conf import DeviceConfig
from device.conf import TellstickConfig
from django.conf import settings

# Create your tests here.

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

class DeviceRestCalls(BasicDeviceTest):
        def test_send_on_command(self):
            client = Client()

            url = reverse('device-command', kwargs={'pk' : self.device.pk})

            response = client.post(
                url,
                {
                    'command' : 'on'
                }
            )

            self.assertEqual(response.status_code, 200)

        def test_should_not_be_able_to_send_command_that_does_not_exist(self):
            client = Client()

            url = reverse('device-command', kwargs={'pk' : self.device.pk})

            response = client.post(
                url,
                {
                    'command' : 'asdf'
                }
            )

            print(response.content)

            self.assertEqual(response.status_code, 400)

            response = client.post(
                url,
                {
                    'not_spelled_correctly' : 'on'
                }
            )

            self.assertEqual(response.status_code, 400)

        def test_should_receive_a_not_found_if_the_id_of_a_device_does_not_exist(self):
            client = Client()

            url = reverse('device-command', kwargs={'pk' : 666})

            response = client.post(
                url,
                {
                    'command' : 'on'
                }
            )

            self.assertEqual(response.status_code, 404)
