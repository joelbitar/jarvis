from django.test import TestCase

from device.models import Device
from node.models import Node
from device.models import DeviceGroup

from event.tests import SignalTestsHelper
from event.receiver import Receiver

from action.models import Action, ActionButton

# Create your tests here.

class TestPropagateSignal(SignalTestsHelper):
    def setUp(self):
        r = Receiver()
        self.signal = r.parse_raw_event('class:command;protocol:arctech;model:selflearning;house:2887766;unit:1;group:0;method:turnon;')
        self.unit = r.get_or_create_unit(self.signal)

        self.node = Node(
            name="Test Node",
            address="http://127.0.0.1",
            api_port=8001
        )

        self.node.save()

        self.device = Device(
            node=self.node,
            protocol=Device.PROTOCOL_ARCHTEC,
            model=Device.MODEL_SELFLEARNING_SWITCH
        )
        self.device.node_device_pk = 1

        self.device.save()

        action = Action(
            name="testAction"
        )
        action.save()

        action.action_devices.add(
            self.device
        )

        button_action = ActionButton(
            action=action,
            button=self.unit
        )
        button_action.save()

        self.button_action = button_action

        action.save()

        self.action = action

    def test_propagate_event(self):
        """
        When an event comes in we should be able to propagate the event through its sender -> unit -> actions

        event ->
                 sender ->
                            unit 1 ->
                                        action 1
                                        action 2

        """

        self.signal.propagate()

        device = Device.objects.get(pk=self.device.pk)

        print('Device state', device.state)

        self.assertEqual(
            device.state,
            1
        )

    def test_propagate_event_if_the_action_is_a_dud(self):
        """
        When an event comes in we should be able to propagate the event through its sender -> unit -> actions

        event ->
                 sender ->
                            unit 1 ->
                                        action 1

        """

        self.action.block_sending = True
        self.action.save()

        self.signal.propagate()

        device = Device.objects.get(pk=self.device.pk)

        print('Device state', device.state)

        self.assertEqual(
            device.state,
            1
        )

    def test_should_execute_on_command_if_button_action_has_filter_on(self):
        self.button_action.command_filter = self.button_action.COMMAND_FILTER_ON
        self.button_action.save()

        self.signal.propagate()

        device = Device.objects.get(pk=self.device.pk)

        self.assertEqual(
            device.state,
            1
        )

    def test_should_not_execute_on_command_if_button_action_has_filter_off(self):
        self.button_action.command_filter = self.button_action.COMMAND_FILTER_OFF
        self.button_action.save()

        self.signal.propagate()

        device = Device.objects.get(pk=self.device.pk)

        self.assertEqual(
            device.state,
            None
        )

    def test_should_execute_off_command_if_button_action_has_filter_off(self):
        self.signal.method = 'turnoff'
        self.signal.save()

        self.button_action.command_filter = self.button_action.COMMAND_FILTER_OFF
        self.button_action.save()

        self.signal.propagate()

        device = Device.objects.get(pk=self.device.pk)

        self.assertEqual(
            device.state,
            0
        )

    def test_should_not_execute_off_command_if_button_action_has_filter_on(self):
        self.signal.method = 'turnoff'
        self.signal.save()

        self.button_action.command_filter = self.button_action.COMMAND_FILTER_ON
        self.button_action.save()

        self.signal.propagate()

        device = Device.objects.get(pk=self.device.pk)

        self.assertEqual(
            device.state,
            None
        )

    def test_should_propagate_to_groups(self):
        device_2 = Device(
            node=self.node,
            protocol=Device.PROTOCOL_ARCHTEC,
            model=Device.MODEL_SELFLEARNING_SWITCH
        )
        device_2.node_device_pk = 44
        device_2.save()


        group = DeviceGroup(
            name='TestGroup'
        )
        group.save()
        group.devices.add(device_2)

        self.action.action_device_groups.add(group)
        self.action.save()

        self.signal.propagate()

        self.assertEqual(Device.objects.all().count(), 2)

        self.assertEqual(
            Device.objects.get(pk=device_2.pk).state,
            1
        )

        for device in Device.objects.all():
            self.assertEqual(
                device.state,
                1
            )


