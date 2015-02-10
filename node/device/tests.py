from django.test import TestCase
from device.models import Device
from device.conf import DeviceConfig
from device.conf import TellstickConfig

# Create your tests here.

class BasicDeviceTest(TestCase):
    def setUp(self):
        self.device = Device(
            name='Test device',
            protocol=Device.PROTOCOL_ARCHTEC,
            model=Device.MODEL_CODESWITCH,
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

class TestDeviceMethodsForConfig(BasicDeviceTest):
    def test_should_get_protocol_string(self):
        self.assertEqual(
            self.device.protocol_string,
            dict(Device.PROTOCOL_CHOICES)[self.device.protocol]
        )

    def test_should_get_model_string(self):
        self.assertEqual(
            self.device.model_string,
            dict(Device.MODEL_CHOICES)[self.device.model]
        )


class TellstickConfigTests(BasicDeviceTest):
    def test_render_tellstick_config_is_a_string(self):
        tc = TellstickConfig(
            devices=Device.objects.all()
        )

        self.assertNotEqual("", tc.render_config())
        self.assertIsNotNone(tc.render_config())

        print(tc.render_config())

