import json

from django.test import TestCase
from django.test.client import Client

from device.models import Device
from device.models import Group
from node.models import Node
from node.models import RequestLog

from node.communicator import NodeDeviceCommunicator
from device.property_generator import DevicePropertyGenerator
from device.property_generator import PropertyValueGenerator

class DeviceModelTestsBase(TestCase):
    def setUp(self):
        n = Node()
        n.address = 'address'
        n.name = 'Test Node'
        n.save()

        d = Device()
        d.name = 'TestDevice'
        d.protocol = Device.PROTOCOL_ARCHTEC
        d.model = Device.MODEL_CODESWITCH
        d.node = n
        d.save()

        g = Group()
        g.name = 'Group'
        g.save()
        g.devices.add(d)
        g.save()

        self.node = n
        self.device = d
        self.group = g

    def refresh(self, obj):
        return obj.__class__.objects.get(pk=obj.pk)


class DeviceTests(DeviceModelTestsBase):
    def test_devices_have_been_created(self):
        self.assertEqual(1, self.device.group_set.all().count())

    def test_should_set_property_iteration_on_model_after_saving_through_generate_properties_method(self):
        dpg = DevicePropertyGenerator(device=self.device)

        self.assertEqual(
            dpg.generate_properties(),
            (self.device, 1)
        )

        self.assertEqual(
            self.refresh(self.device).property_iteration,
            1
        )

    def test_should_set_unique_properties_on_two_devices(self):
        d = Device(
            name='Archtec Codeswitch',
            protocol=Device.PROTOCOL_ARCHTEC,
            model=Device.MODEL_CODESWITCH,
            node=self.node,
        )

        d.save()

        dpg = DevicePropertyGenerator(device=d)
        device, iteration = dpg.generate_properties()

        self.assertEqual(
            iteration,
            1
        )

        self.assertEqual(
            device.house,
            'A'
        )
        self.assertEqual(
            device.unit,
            1
        )

        d = Device(
            name='Archtec Codeswitch 2',
            protocol=Device.PROTOCOL_ARCHTEC,
            model=Device.MODEL_CODESWITCH,
            node=self.node,
        )

        d.save()

        dpg = DevicePropertyGenerator(device=d)
        device, iteration = dpg.generate_properties()

        self.assertEqual(
            iteration,
            2
        )

        self.assertEqual(
            device.house,
            'A'
        )
        self.assertEqual(
            device.unit,
            2
        )

    def test_should_not_set_the_same_properties_if_generate_property_iteration_on_previous_devices_has_been_meddled_with(self):
        dpg = DevicePropertyGenerator(device=self.device)
        dpg.generate_properties()
        self.device.property_iteration = None
        self.device.save()

        d = Device(
            name='Archtec Codeswitch',
            protocol=Device.PROTOCOL_ARCHTEC,
            model=Device.MODEL_CODESWITCH,
            node=self.node,
        )

        d.save()

        dpg = DevicePropertyGenerator(device=d)
        device, iteration = dpg.generate_properties()

        self.assertEqual(
            iteration,
            2
        )

    def test_is_device_unique_should_return_false_if_there_is_a_device_with_that_unit_and_house(self):
        device = Device(
            name='Archtec Codeswitch',
            protocol=Device.PROTOCOL_ARCHTEC,
            model=Device.MODEL_CODESWITCH,
            node=self.node,
            house="A",
            unit=1
        )
        device.save()

        dpg = DevicePropertyGenerator(device=self.device)
        self.assertFalse(
            dpg.is_device_unique(
                device,
                {
                    'house': 'A',
                    'unit': 1
                }
            )
        )

    def test_should_set_iteration_to_second_even_if_properties_has_been_manually_set(self):
        Device(
            name='Archtec Codeswitch',
            protocol=Device.PROTOCOL_ARCHTEC,
            model=Device.MODEL_CODESWITCH,
            node=self.node,
            house="A",
            unit=1
        ).save()

        d = Device(
            name='Archtec Codeswitch',
            protocol=Device.PROTOCOL_ARCHTEC,
            model=Device.MODEL_CODESWITCH,
            node=self.node,
        )

        d.save()

        dpg = DevicePropertyGenerator(device=d)
        device, iteration = dpg.generate_properties()

        self.assertEqual(
            iteration,
            2
        )


    def test_should_only_select_max_iteration_from_within_model_and_protocol_group(self):
        archtec_codeswitch = Device(
            name='Archtec Codeswitch',
            protocol=Device.PROTOCOL_ARCHTEC,
            model=Device.MODEL_CODESWITCH,
            node=self.node,
            property_iteration=1000
        )
        archtec_codeswitch.save()

        archtec_selflearningcodeswitch = Device(
            name='Archtec Codeswitch',
            protocol=Device.PROTOCOL_ARCHTEC,
            model=Device.MODEL_SELFLEARNING_SWITCH,
            node=self.node,
            property_iteration=100
        )
        archtec_selflearningcodeswitch.save()

        archtec_selflearningdimmer = Device(
            name='Archtec Codeswitch',
            protocol=Device.PROTOCOL_ARCHTEC,
            model=Device.MODEL_SELFLEARNING_DIMMER,
            node=self.node,
            property_iteration=10
        )
        archtec_selflearningdimmer.save()

        dpg = DevicePropertyGenerator(device=archtec_codeswitch)
        self.assertEqual(
            dpg.get_max_property_iteration(),
            1000
        )
        dpg = DevicePropertyGenerator(device=archtec_selflearningcodeswitch)
        self.assertEqual(
            dpg.get_max_property_iteration(),
            100
        )
        dpg = DevicePropertyGenerator(device=archtec_selflearningdimmer)
        self.assertEqual(
            dpg.get_max_property_iteration(),
            10
        )

    def test_auto_generate_properties_on_archtec_codeswitch(self):
        self.device.model = Device.MODEL_CODESWITCH
        self.device.protocol = Device.PROTOCOL_ARCHTEC
        self.device.save()

        dpg = DevicePropertyGenerator(device=self.device)
        dpg.generate_properties()

        d = self.refresh(self.device)
        self.assertEqual(
            d.house,
            'A'
        )
        self.assertEqual(
            d.unit,
            '1'
        )

    def test_auto_generate_properties_on_archtec_selflearningdimmer(self):
        self.device.model = Device.MODEL_SELFLEARNING_DIMMER
        self.device.protocol = Device.PROTOCOL_ARCHTEC
        self.device.save()

        dpg = DevicePropertyGenerator(device=self.device)
        dpg.generate_properties()

        d = self.refresh(self.device)
        self.assertEqual(
            d.house,
            '1'
        )
        self.assertEqual(
            d.unit,
            '1'
        )

    def test_auto_generate_properties_on_archtec_selflearningswitch(self):
        self.device.model = Device.MODEL_SELFLEARNING_SWITCH
        self.device.protocol = Device.PROTOCOL_ARCHTEC
        self.device.save()

        dpg = DevicePropertyGenerator(device=self.device)
        dpg.generate_properties()

        d = self.refresh(self.device)
        self.assertEqual(
            d.house,
            '1'
        )
        self.assertEqual(
            d.unit,
            '1'
        )


    def test_auto_generate_properties_on_archtec_codeswitch_when_one_hundred_already_exists(self):
        self.device.model = Device.MODEL_CODESWITCH
        self.device.protocol = Device.PROTOCOL_ARCHTEC
        self.device.property_iteration = 99
        self.device.save()

        dpg = DevicePropertyGenerator(device=self.device)
        dpg.generate_properties()

        d = self.refresh(self.device)
        self.assertEqual(
            d.house,
            'G'
        )
        self.assertEqual(
            d.unit,
            '4'
        )

    def test_property_value_generator_min_value_not_zero_should_generate_one_as_first_value(self):
        """
        When having a 'min' value that is not the lowest, the first value should be that value
        """
        pvg = PropertyValueGenerator(
            {
                'name': 'test1',
                'type': PropertyValueGenerator.TYPE_INTEGER,
                'min': 1,
                'max': 16,
            }
        )
        self.assertEqual(pvg.get_possibilities_count(
            pvg.get_property_conf('test1')
        ), 16)

        self.assertEqual(
            pvg.get_total_possibilities_count(),
            16
        )

        self.assertEqual(
            pvg(),
            {
                'test1': 1,
            }
        )

    def test_property_value_generator_generate_for_integer_property(self):
        pvg = PropertyValueGenerator(
            {
                'name': 'test1',
                'type': PropertyValueGenerator.TYPE_INTEGER,
                'min': 0,
                'max': 15,
            },
            {
                'name': 'test2',
                'type': PropertyValueGenerator.TYPE_CHARACTER,
                'min': 'a',
                'max': 'c'
            }
        )
        self.assertEqual(pvg.get_possibilities_count(
            pvg.get_property_conf('test1')
        ), 16)

        self.assertEqual(
            pvg.get_total_possibilities_count(),
            48
        )

        self.assertEqual(
            pvg(),
            {
                'test1': 0,
                'test2': 'A',
            }
        )

        self.assertEqual(
            pvg(),
            {
                'test1': 1,
                'test2': 'A',
            }
        )

    def test_property_value_generator_generate_for_dual_character_properties(self):
        pvg = PropertyValueGenerator(
            {
                'name': 'test1',
                'type': PropertyValueGenerator.TYPE_CHARACTER,
                'min': 'a',
                'max': 'c'
            },
            {
                'name': 'test2',
                'type': PropertyValueGenerator.TYPE_CHARACTER,
                'min': 'a',
                'max': 'f'
            }
        )

        self.assertEqual(
            pvg.get_total_possibilities_count(),
            18
        )

        self.assertEqual(pvg.get_possibilities_count(
            pvg.get_property_conf('test1')
        ), 3)

        self.assertEqual(
            pvg(),
            {
                'test1': 'A',
                'test2': 'A'
            }
        )

        self.assertEqual(
            pvg(),
            {
                'test1': 'B',
                'test2': 'A'
            }
        )

        self.assertEqual(
            pvg(),
            {
                'test1': 'C',
                'test2': 'A'
            }
        )

        self.assertEqual(
            pvg(),
            {
                'test1': 'A',
                'test2': 'B'
            }
        )

        self.assertEqual(
            pvg(),
            {
                'test1': 'B',
                'test2': 'B'
            }
        )

        pvg.reset_iteration()

        for i in range(10):
            pvg()

        self.assertEqual(
            pvg(),
            {
                'test1': 'B',
                'test2': 'D'
            }
        )

        pvg.reset_iteration()

        for i in range(18):
            pvg()

        self.assertRaises(
            ValueError,
            pvg
        )



class NodeCrudCommunicationTests(DeviceModelTestsBase):
    def test_create_device_on_node_rest_call(self):
        nd = NodeDeviceCommunicator(device=self.device)

        def fake_get_response(url, method, data):
            return 201, {
                'id' : 1001
            }

        nd.get_response = fake_get_response
        self.assertTrue(nd.create())
        self.assertEqual(self.refresh(self.device).node_device_pk, 1001)

        self.assertEqual(
            1,
            RequestLog.objects.all().count()
        )

        r = RequestLog.objects.get(pk=1)
        self.assertEqual(
            r.url,
            self.node.address + '/devices/'
        )

        self.assertIsNotNone(
            r.response_data,
        )

        self.assertJSONEqual(
            r.response_data,
            json.dumps({'id': 1001})
        )

        self.assertEqual(
            r.method,
            'post'
        )

        self.assertEqual(
            r.response_status_code,
            201
        )

    def test_should_not_be_able_to_execute_requests_on_device_that_has_no_node_id(self):
        nd = NodeDeviceCommunicator(device=self.device)

        self.assertRaises(
            ValueError,
            nd.update
        )

        self.assertRaises(
            ValueError,
            nd.delete
        )

    def test_delete_device_on_node_rest_call(self):
        nd = NodeDeviceCommunicator(device=self.device)

        def fake_get_response(url, method, data):
            return 200, {}

        nd.get_response = fake_get_response

        self.device.node_device_pk = 1001
        self.device.save()

        self.assertTrue(nd.delete())

        self.assertEqual(
            1,
            RequestLog.objects.all().count()
        )

        r = RequestLog.objects.get(pk=1)
        self.assertEqual(
            r.url,
            self.node.address + '/devices/{node_device_pk}/'.format(node_device_pk=self.device.node_device_pk)
        )

        self.assertIsNotNone(
            r.response_data,
        )

        self.assertJSONEqual(
            r.response_data,
            json.dumps({})
        )

        self.assertEqual(
            r.method,
            'delete'
        )

        self.assertEqual(
            r.response_status_code,
            200
        )

    def test_update_device_on_node_rest_call(self):
        nd = NodeDeviceCommunicator(device=self.device)

        def fake_get_response(url, method, data):
            return 200, {}

        nd.get_response = fake_get_response

        self.device.node_device_pk = 1001
        self.device.save()

        self.assertTrue(nd.update())

        self.assertEqual(
            1,
            RequestLog.objects.all().count()
        )

        r = RequestLog.objects.get(pk=1)
        self.assertEqual(
            r.url,
            self.node.address + '/devices/{node_device_pk}/'.format(node_device_pk=self.device.node_device_pk)
        )

        self.assertIsNotNone(
            r.response_data,
        )

        self.assertJSONEqual(
            r.response_data,
            json.dumps({})
        )

        self.assertEqual(
            r.method,
            'put'
        )

        self.assertEqual(
            r.response_status_code,
            200
        )


class NodeControlCommunicationsTests(DeviceModelTestsBase):
    def setUp(self):
        super(NodeControlCommunicationsTests, self).setUp()

        self.device.node_device_pk = 1001
        self.device.save()

    def test_send_learn_command(self):
        nd = NodeDeviceCommunicator(device=self.device)

        def fake_get_response(url, method, data):
            if data != {'command': 'learn'}:
                print(data)
                raise ValueError()
            return 200, {}

        nd.get_response = fake_get_response
        self.assertTrue(nd.learn())

        self.assertEqual(
            1,
            RequestLog.objects.all().count()
        )

        r = RequestLog.objects.get(pk=1)
        self.assertEqual(
            r.url,
            self.node.address + '/devices/{node_device_pk}/command/'.format(node_device_pk=self.device.node_device_pk)
        )

        self.assertIsNotNone(
            r.response_data,
        )

        self.assertEqual(
            r.response_status_code,
            200
        )

    def test_send_off_command(self):
        nd = NodeDeviceCommunicator(device=self.device)

        def fake_get_response(url, method, data):
            if data != {'command': 'off'}:
                raise ValueError()
            return 200, {}

        nd.get_response = fake_get_response
        self.assertTrue(nd.turn_off())

        self.assertEqual(
            1,
            RequestLog.objects.all().count()
        )

        r = RequestLog.objects.get(pk=1)
        self.assertEqual(
            r.url,
            self.node.address + '/devices/{node_device_pk}/command/'.format(node_device_pk=self.device.node_device_pk)
        )

        self.assertIsNotNone(
            r.response_data,
        )

        self.assertEqual(
            r.response_status_code,
            200
        )

    def test_send_on_command(self):
        nd = NodeDeviceCommunicator(device=self.device)

        def fake_get_response(url, method, data):
            if data != {'command': 'on'}:
                print(data)
                raise ValueError()
            return 200, {}

        nd.get_response = fake_get_response
        self.assertTrue(nd.turn_on())

        self.assertEqual(
            1,
            RequestLog.objects.all().count()
        )

        r = RequestLog.objects.get(pk=1)
        self.assertEqual(
            r.url,
            self.node.address + '/devices/{node_device_pk}/command/'.format(node_device_pk=self.device.node_device_pk)
        )

        self.assertIsNotNone(
            r.response_data,
        )

        self.assertEqual(
            r.response_status_code,
            200
        )

class HubDeviceRestTests(DeviceModelTestsBase):
    """
    Tests REST interfaces on HUB (they just proxy, but they should exist anywho)
    """
    def setUp(self):
        super(HubDeviceRestTests, self).setUp()

        self.device.node_device_pk = 1001
        self.device.save()

        self.client = Client()

    def test_should_get_all_devices(self):
        for i in range(10):
            Device(
                    name='TestDevice {i}'.format(i=i),
                    node_device_pk=100 + i,
                    protocol=Device.PROTOCOL_ARCHTEC,
                    model=Device.MODEL_SELFLEARNING_SWITCH,
                    node=self.node
                ).save()

        self.assertTrue(False)

    def test_should_get_single_device(self):
        response = self.client.get(
            '/devices/{device_id}/'.format(device_id=self.device.id)
        )

        self.assertEqual(response.status_code, 200)

        self.assertJSONEqual(
                response.content.decode('utf-8'),
                json.dumps(
                    {
                        'id' : self.device.id,
                        'model_string' : self.device.model_string,
                        'protocol_string': self.device.protocol_string,
                    }
                )
            )

        # No Logging should take place
        self.assertEqual(
            0,
            RequestLog.objects.all().count()
        )

    def test_should_get_ok_response_when_sending_create(self):
        self.assertTrue(False)

        self.assertEqual(
            1,
            RequestLog.objects.all().count()
        )

    def test_should_get_ok_response_when_sending_update(self):
        self.assertTrue(False)

        self.assertEqual(
            1,
            RequestLog.objects.all().count()
        )


    def test_should_get_ok_response_when_sending_delete(self):
        self.assertTrue(False)

        self.assertEqual(
            1,
            RequestLog.objects.all().count()
        )


    def test_should_get_ok_response_when_sending_command_learn(self):
        self.assertTrue(False)
        
        self.assertEqual(
            1,
            RequestLog.objects.all().count()
        )


    def test_should_get_ok_response_when_sending_command_on(self):
        self.assertTrue(False)

        self.assertEqual(
            1,
            RequestLog.objects.all().count()
        )


    def test_should_get_ok_response_when_sending_command_off(self):
        self.assertTrue(False)

        self.assertEqual(
            1,
            RequestLog.objects.all().count()
        )

