__author__ = 'joel'
from device.message.message import Message
from device.models import Device


class DeviceCommandMessage(Message):
    __device = None
    __command_name = None
    __command_data = {}

    def __init__(self, *args, **kwargs):
        super(DeviceCommandMessage, self).__init__(*args, **kwargs)
        self.__device = None
        self.__command_name = None
        self.__command_data = {}

    @property
    def device(self):
        if self.__device is not None:
            return self.__device

        self.__device = Device.objects.get(pk=self.message_obj['device_id'])

        return self.__device

    @device.setter
    def device(self, device_obj):
        self.__device = device_obj

    @property
    def command_data(self):
        return self.message_obj.get(
            'command_data', {}
        )

    @property
    def command_name(self):
        return self.message_obj['command_name']

    @command_name.setter
    def command_name(self, command_name):
        self.__command_name = command_name

    def to_json(self):
        self.__json_obj = {
            'device_id': self.__device.pk,
            'command_name': self.__command_name,
            'command_data': self.__command_data or {}
        }

        return self.__json_obj

    def set_command_data(self, key, value):
        self.__command_data[key] = value

    def execute(self):
        return self.device.commands.execute_command(
            self.command_name,
            **self.command_data
        )

