import json

from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.core.urlresolvers import reverse

from django.test import TestCase
from django.test.client import Client

from device.models import Device
from device.models import DeviceGroup
from node.models import Node
from node.models import RequestLog

from node.communicator import NodeDeviceCommunicator
from device.property_generator import DevicePropertyGenerator
from device.property_generator import PropertyValueGenerator

from button.models import Button


class HasLoggedInClientBase(TestCase):
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

        self.maxDiff = 5000
        self.logged_in_client = client

        superuser_client = Client()

        self.admin_user = User.objects.create_superuser(
            username='admin',
            password='admin',
            email='admin@example.com',
        )

        superuser_client.login(
            username='admin',
            password='admin',
        )

        self.superuser_client = superuser_client


class DeviceModelTestsBase(HasLoggedInClientBase):
    def setUp(self):
        super(DeviceModelTestsBase, self).setUp()
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

        g = DeviceGroup()
        g.name = 'Group'
        g.save()
        g.devices.add(d)
        g.save()

        self.node = n
        self.device = d
        self.group = g


    def refresh(self, obj):
        return obj.__class__.objects.get(pk=obj.pk)


class DeviceBasicModelAttributesTests(DeviceModelTestsBase):
    def test_should_have_a_blank_category_on_device(self):
        self.assertEqual(
            self.device.category,
            None
        )

    def test_should_reset_learnt_on_node_if_node_changed(self):
        self.device.learnt_on_node = True
        self.device.save()

        n2 = Node(
            address='http://127.0.0.2',
            name='Other node'
        )

        n2.save()

        self.device.node = n2
        self.device.save()

        self.assertFalse(
            Device.objects.get(pk=self.device.pk).learnt_on_node
        )


class DeviceModelTests(TestCase):
    def test_create_should_have_set_properties(self):
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

        self.assertEqual(d.house, 'A')
        self.assertEqual(d.unit, 1)

    def test_should_not_re_set_properties(self):
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

        d.save()

        self.assertEqual(d.house, 'A')
        self.assertEqual(d.unit, 1)


class DevicePropertySetterTests(TestCase):
    def setUp(self):
        n = Node()
        n.address = 'address'
        n.name = 'Test Node'
        n.save()

        self.node = n

    def test_should_set_unique_properties(self):
        for i in range(1,5):
            d = Device(
                    name='Archtec Codeswitch',
                    protocol=Device.PROTOCOL_ARCHTEC,
                    model=Device.MODEL_CODESWITCH,
                    node=self.node,
                )

            d.save()

            self.assertEqual(
                d.house,
                'A'
            )

            self.assertEqual(
                d.unit,
                i
            )



    def test_should_set_iteration(self):
        for i in range(1,5):
            d = Device(
                    name='Archtec Codeswitch',
                    protocol=Device.PROTOCOL_ARCHTEC,
                    model=Device.MODEL_CODESWITCH,
                    node=self.node,
                )

            d.save()

            self.assertEqual(
                d.property_iteration,
                i
            )


class DeviceTests(DeviceModelTestsBase):
    def test_devices_have_been_created(self):
        self.assertEqual(1, self.device.devicegroup_set.all().count())

    def test_should_set_property_iteration_on_model_after_saving_through_generate_properties_method(self):
        # Should be first if we just look at the newly created device
        self.assertEqual(
            self.refresh(self.device).property_iteration,
            1
        )

        dpg = DevicePropertyGenerator(device=self.device)

        self.assertEqual(
            dpg.generate_properties(),
            ({
                'unit': 2,
                'house' : 'A'
            }, 2)
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

        print('\n')
        print('Generating properties in test class')
        dpg = DevicePropertyGenerator(device=d)
        properties, iteration = dpg.generate_properties()

        self.assertEqual(d.pk, None)

        self.assertEqual(
            iteration,
            2
        )

        self.assertEqual(
            properties['unit'],
            2
        )
        
        self.assertEqual(
            properties['house'],
            'A'
        )

        d.unit = properties['unit']
        d.house = properties['house']

        d.save()

        d = Device(
            name='Archtec Codeswitch 2',
            protocol=Device.PROTOCOL_ARCHTEC,
            model=Device.MODEL_CODESWITCH,
            node=self.node,
        )

        d.save()

        self.assertEqual(
            d.property_iteration,
            3
        )

        self.assertEqual(
            d.house,
            'A'
        )

        self.assertEqual(
            d.unit,
            3
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
            3
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
        d = Device(
            name='Archtec Codeswitch',
            protocol=Device.PROTOCOL_ARCHTEC,
            model=Device.MODEL_CODESWITCH,
            node=self.node,
        )
        d.save()

        d = Device(
            name='Archtec Codeswitch',
            protocol=Device.PROTOCOL_ARCHTEC,
            model=Device.MODEL_CODESWITCH,
            node=self.node,
        )
        d.save()

        dpg = DevicePropertyGenerator(device=d)
        properties, iteration = dpg.generate_properties()

        self.assertEqual(
            iteration,
            4
        )

    def test_should_only_select_max_iteration_from_within_model_and_protocol_group(self):
        archtec_codeswitch = Device(
            name='Archtec Codeswitch',
            protocol=Device.PROTOCOL_ARCHTEC,
            model=Device.MODEL_CODESWITCH,
            node=self.node,
        )
        archtec_codeswitch.save()
        archtec_codeswitch.property_iteration = 1000
        archtec_codeswitch.save()

        archtec_selflearningcodeswitch = Device(
            name='Archtec Codeswitch',
            protocol=Device.PROTOCOL_ARCHTEC,
            model=Device.MODEL_SELFLEARNING_SWITCH,
            node=self.node,
        )
        archtec_selflearningcodeswitch.save()
        archtec_selflearningcodeswitch.property_iteration=100
        archtec_selflearningcodeswitch.save()

        archtec_selflearningdimmer = Device(
            name='Archtec Codeswitch',
            protocol=Device.PROTOCOL_ARCHTEC,
            model=Device.MODEL_SELFLEARNING_DIMMER,
            node=self.node,
        )
        archtec_selflearningdimmer.save()
        archtec_selflearningdimmer.property_iteration=10
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
        properties, iteration = dpg.generate_properties()

        d = self.refresh(self.device)
        self.assertEqual(
            str(properties['house']),
            '2000'
        )
        self.assertEqual(
            str(properties['unit']),
            '2'
        )

    def test_auto_generate_properties_on_archtec_selflearningswitch(self):
        self.device.model = Device.MODEL_SELFLEARNING_SWITCH
        self.device.protocol = Device.PROTOCOL_ARCHTEC
        self.device.save()

        dpg = DevicePropertyGenerator(device=self.device)
        properties, iteration = dpg.generate_properties()

        d = self.refresh(self.device)
        self.assertEqual(
            properties['house'],
            1000
        )
        self.assertEqual(
            properties['unit'],
            2
        )


    def test_auto_generate_properties_on_archtec_codeswitch_when_one_hundred_already_exists(self):
        self.device.model = Device.MODEL_CODESWITCH
        self.device.protocol = Device.PROTOCOL_ARCHTEC
        self.device.property_iteration = 99
        self.device.save()

        dpg = DevicePropertyGenerator(device=self.device)
        properties, iteration = dpg.generate_properties()

        d = self.refresh(self.device)
        self.assertEqual(
            str(properties['house']),
            'G'
        )
        self.assertEqual(
            str(properties['unit']),
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

        def fake_get_response(*args, **kwargs):
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

        def fake_get_response(*args, **kwargs):
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

        def fake_get_response(*args, **kwargs):
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

        def fake_get_response(url, method, data, auth_token):
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
            self.node.address + '/devices/{node_device_pk}/execute/'.format(node_device_pk=self.device.node_device_pk)
        )

        self.assertIsNotNone(
            r.response_data,
        )

        self.assertEqual(
            r.response_status_code,
            200
        )

        device = self.refresh(self.device)

        self.assertTrue(
            device.learnt_on_node
        )

    def test_send_off_command(self):
        nd = NodeDeviceCommunicator(device=self.device)

        def fake_get_response(url, method, data, auth_token):
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
            self.node.address + '/devices/{node_device_pk}/execute/'.format(node_device_pk=self.device.node_device_pk)
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

        def fake_get_response(url, method, data, auth_token):
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
            self.node.address + '/devices/{node_device_pk}/execute/'.format(node_device_pk=self.device.node_device_pk)
        )

        self.assertIsNotNone(
            r.response_data,
        )

        self.assertEqual(
            r.response_status_code,
            200
        )


class HubDeviceOptionsTests(TestCase):
    def test_get_options_for_device(self):
        self.user = User.objects.create_user(
            username='test',
            password='test'
        )

        client = Client()
        client.login(
            username='test',
            password='test'
        )

        response = client.get(
            reverse('device-options')
        )

        self.maxDiff = 5000
        self.assertJSONEqual(
                response.content.decode('utf-8'),
                json.dumps(
                    {
                        'protocol_model_options' : [
                            {
                                'protocol' : {
                                    'id' : Device.PROTOCOL_ARCHTEC,
                                    'name' : 'arctech',
                                    'models' : [
                                        {
                                            'id': Device.MODEL_CODESWITCH,
                                            'name': 'Code switch',
                                            },
                                        {
                                            'id': Device.MODEL_BELL,
                                            'name': 'Bell',
                                            },
                                        {
                                            'id': Device.MODEL_SELFLEARNING_SWITCH,
                                            'name': 'Selflearning switch',
                                            },
                                        {
                                            'id': Device.MODEL_SELFLEARNING_DIMMER,
                                            'name': 'Selflearning dimmer',
                                            },
                                        ]
                                },
                            },
                        ],
                        'button_type_options' : [
                            {
                                'id': Button.BUTTON_TYPE_BUTTON,
                                'name': str(_('Button')),
                            },
                            {
                                'id': Button.BUTTON_TYPE_MOTION_SENSOR,
                                'name': str(_('Motion sensor'))
                            },
                            {
                                'id': Button.BUTTON_TYPE_DOOR_SENSOR,
                                'name': str(_('Door sensor')),
                            },
                        ]
                    }
                )
            )

class HubDeviceRestTests(DeviceModelTestsBase):
    """
    Tests REST interfaces on HUB (they just proxy, but they should exist anywho)
    """
    def setUp(self):
        super(HubDeviceRestTests, self).setUp()

        self.device.node_device_pk = 1001
        self.device.save()

    def test_should_get_all_devices(self):
        for i in range(10):
            Device(
                    name='TestDevice {i}'.format(i=i),
                    node_device_pk=100 + i,
                    protocol=Device.PROTOCOL_ARCHTEC,
                    model=Device.MODEL_SELFLEARNING_SWITCH,
                    node=self.node
                ).save()
        
        response = self.logged_in_client.get(
            reverse('device-list')
        )

        response_json = json.loads(response.content.decode('utf-8'))

        self.assertEqual(len(response_json), Device.objects.all().count())

    def test_should_get_single_device(self):
        response = self.logged_in_client.get(
            reverse('device-detail', kwargs={'pk': self.device.pk}),
        )

        self.assertEqual(response.status_code, 200)

        self.assertJSONEqual(
                response.content.decode('utf-8'),
                json.dumps(
                    {
                        'id' : self.device.id,
                        'model_string' : self.device.model_string,
                        'protocol_string': self.device.protocol_string,
                        'code': None,
                        'controller': None,
                        'description': '',
                        'devices': None,
                        'fade': None,
                        'house': 'A',
                        'model': self.device.model,
                        'name': 'TestDevice',
                        'node': self.device.node.pk,
                        'node_device_pk': 1001,
                        'property_iteration': 1,
                        'protocol': self.device.protocol,
                        'state': None,
                        'system': None,
                        'unit': '1',
                        'units': None,
                        'category': None,
                        'written_to_conf_on_node': False,
                        'learnt_on_node': False,
                        'is_dimmable': False,
                    }
                )
            )

        # No Logging should take place
        self.assertEqual(
            0,
            RequestLog.objects.all().count()
        )

    def test_should_get_ok_response_when_sending_create(self):
        response = self.logged_in_client.put(
            reverse('device-detail', kwargs={'pk': self.device.pk}),
            json.dumps({
                'name' : 'New testDevice',
                'model': self.device.model,
                'node': self.device.node.pk,
                'property_iteration': None,
                'protocol': self.device.protocol,

            }),
            content_type='application/json'
        )

        self.assertEqual(200, response.status_code)

        self.assertEqual(
            0,
            RequestLog.objects.all().count()
        )

        self.assertEqual(
            0,
            RequestLog.objects.all().count()
        )

        self.assertEqual(Device.objects.all().count(), 1)

    def test_should_have_populated_properites(self):
        self.test_should_get_ok_response_when_sending_create()

        d = Device.objects.all()[0]

        self.assertEqual(d.house, 'A')
        self.assertEqual(d.unit, '1')


    def test_should_get_ok_response_when_sending_update(self):
        response = self.logged_in_client.put(
            reverse('device-detail', kwargs={'pk': self.device.pk}),
            json.dumps({
                'name' : 'New testDevice',
                'model': self.device.model,
                'node': self.device.node.pk,
                'property_iteration': None,
                'protocol': self.device.protocol,

            }),
            content_type='application/json'
        )

        self.assertEqual(200, response.status_code)

        self.assertEqual(
            0,
            RequestLog.objects.all().count()
        )


    def test_should_get_ok_response_when_sending_delete(self):
        response = self.logged_in_client.delete(
                reverse('device-detail', kwargs={'pk': self.device.pk}),
                content_type='application/json'
        )

        self.assertEqual(
            0,
            RequestLog.objects.all().count()
        )

        self.assertEqual(Device.objects.all().count(), 0)

    def test_should_get_forbidden_if_not_admin_response_when_sending_command_learn(self):
        self.assertFalse(
            self.user.is_superuser
        )
        response = self.logged_in_client.get(
            reverse('device-learn', kwargs={'pk': self.device.pk}),
        )

        self.assertEqual(response.status_code, 403)

        self.assertEqual(
            0,
            RequestLog.objects.all().count()
        )

    def test_should_get_ok_response_when_sending_command_learn_when_admin(self):
        response = self.superuser_client.get(
            reverse('device-learn', kwargs={'pk': self.device.pk}),
        )

        self.assertEqual(response.status_code, 200)
        
        self.assertEqual(
            1,
            RequestLog.objects.all().count()
        )

    def test_should_get_ok_response_when_sending_command_on(self):
        response = self.logged_in_client.get(
             reverse('device-on', kwargs={'pk': self.device.pk}),
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            self.refresh(self.device).state,
            1
        )

        self.assertEqual(
            1,
            RequestLog.objects.all().count()
        )

    def test_should_get_ok_response_when_sending_command_dimm_with_values_within_range(self):
        response = self.logged_in_client.get(
                reverse('device-dim', kwargs={'pk': self.device.pk, 'dimlevel' : 50}),
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            1,
            RequestLog.objects.all().count()
        )

        d = self.refresh(self.device)

        self.assertEqual(
            d.state,
            50
        )

    def test_should_get_ok_response_when_sending_command_off(self):
        response = self.logged_in_client.get(
            reverse('device-off', kwargs={'pk': self.device.pk}),
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            self.refresh(self.device).state,
            0
        )

        self.assertEqual(
            1,
            RequestLog.objects.all().count()
        )


class DeviceGroupAPITests(DeviceModelTestsBase):
    def setUp(self):
        super(DeviceGroupAPITests, self).setUp()

        self.device.node_device_pk = 666
        self.device.save()

    def test_should_get_groups(self):
        response = self.logged_in_client.get(
            reverse('devicegroup-list')
        )

        self.assertJSONEqual(
            response.content.decode('utf-8'),
            json.dumps(
                [
                    {
                        'id': self.group.pk,
                        'name': self.group.name,
                        'state': 0,
                        'devices': [
                            {
                                'id': self.device.pk,
                                'name': self.device.name,
                            },
                        ]
                    },
                ]
            )
        )

    def test_should_get_ok_response_when_set_group_to_on(self):
        response = self.logged_in_client.get(
            reverse('devicegroup-on', kwargs={
                'pk': self.group.pk
            })
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_should_get_ok_response_when_set_group_to_off(self):
        response = self.logged_in_client.get(
            reverse('devicegroup-off', kwargs={
                'pk': self.group.pk
            })
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_should_set_device_states_when_set_group_to_on(self):
        self.assertIsNone(
            self.device.state
        )
        response = self.logged_in_client.get(
            reverse('devicegroup-on', kwargs={
                'pk': self.group.pk
            })
        )

        self.assertEqual(
            self.refresh(self.device).state,
            1
        )

    def test_should_set_device_states_when_set_group_to_off(self):
        response = self.logged_in_client.get(
            reverse('devicegroup-off', kwargs={
                'pk': self.group.pk
            })
        )

        self.assertEqual(
            self.refresh(self.device).state,
            0
        )


class DeviceGroupStateTests(DeviceModelTestsBase):
    def setUp(self):
        super(DeviceGroupStateTests, self).setUp()

        self.device.node_device_pk = 666
        self.device.save()

        self.device2 = Device(
            name='device2',
            protocol=Device.PROTOCOL_ARCHTEC,
            model=Device.MODEL_SELFLEARNING_DIMMER,
            node=self.node,
        )
        self.device2.save()

        self.device3 = Device(
            name='device3',
            protocol=Device.PROTOCOL_ARCHTEC,
            model=Device.MODEL_SELFLEARNING_SWITCH,
            node=self.node,
        )
        self.device3.save()

        self.group.devices.add(self.device2)
        self.group.devices.add(self.device3)

        self.assertEqual(
            self.group.devices.all().count(),
            3
        )

        Device.objects.all().update(
            node_device_pk=666
        )

    def helper_get_device_group_state(self):
        response = self.logged_in_client.get(
            reverse('devicegroup-list')
        )

        return json.loads(response.content.decode('utf-8'))[0]['state']

    def test_should_have_device_group_state_false_if_all_devices_are_none(self):
        self.assertEqual(
            self.helper_get_device_group_state(),
            0
        )

    def test_should_have_state_true_if_all_devices_are_on(self):
        Device.objects.all().update(
            state=1
        )
        self.assertEqual(
            self.helper_get_device_group_state(),
            1
        )

    def test_should_have_state_true_if_one_device_is_on(self):
        self.device.state = 1
        self.device.save()

        self.assertEqual(
            self.helper_get_device_group_state(),
            1
        )

    def test_should_have_state_true_if_only_one_device_dimmer_is_not_off(self):
        self.device2.state = 33
        self.device2.save()

        self.assertEqual(
            self.group.state,
            1
        )

        self.assertEqual(
            self.helper_get_device_group_state(),
            1
        )

    def test_should_have_state_false_if_all_devices_are_off(self):
        Device.objects.all().update(
            state=0
        )
        self.assertEqual(
            self.helper_get_device_group_state(),
            0
        )

    def test_should_not_have_state_true_if_there_is_no_devices(self):
        Device.objects.all().delete()
        self.assertNotEqual(
            self.helper_get_device_group_state(),
            1
        )


    def test_should_set_dimmer_to_full_effect_when_sending_to_command_on_on_group(self):
        response = self.logged_in_client.get(
            reverse('devicegroup-on', kwargs={
                'pk': self.group.pk
            })
        )

        self.assertEqual(
            self.refresh(self.device2).state,
            255
        )


