from django.test import TestCase
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
    pass
