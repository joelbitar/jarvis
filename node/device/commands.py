__author__ = 'joel'
import os
from subprocess import call
from django.core import mail


class CommandError(Exception):
    pass


class BaseCommand(object):
    def is_in_test_mode(self):
        if hasattr(mail, 'outbox'):
           return True
        else:
            return False


class CommandDispatcher(BaseCommand):
    COMMAND_NAME_WHITE_LIST = ['on', 'off', 'learn', 'dim']
    __device = None
    __send_commands = True

    def __init__(self, device):
        self.__device = device

        # If we are in Test mode we disable sending commands
        self.__send_commands = not self.is_in_test_mode() 
        
    @property
    def send_commands(self):
        return self.__send_commands

    @property
    def device(self):
        return self.__device

    def execute_command(self, command_name, **kwargs):
        if command_name not in self.COMMAND_NAME_WHITE_LIST:
            raise CommandError('command name "{command_name}" is not in white list'.format(command_name=command_name))

        # Command name
        command = ['tdtool']

        # If dim command add --dimlevel
        if command_name == 'dim':
            command += ['--dimlevel', str(kwargs.get('dimlevel'))]

        # Add the acutal command name like on, off, learn etc
        command += ['--{command_name}'.format(command_name=command_name)]

        # Add the device ID
        command += [str(self.device.pk)]

        if self.send_commands:
            call(command)
        else:
            print('Does not call command, in test mode. $ ' + " ".join(command))

        return True

    def learn(self):
        self.execute_command('learn')

    def turn_on(self):
        self.execute_command('on')

    def turn_off(self):
        self.execute_command('off')

    def dim(self, dimlevel):
        self.execute_command(
            'dim',
            dimlevel=dimlevel
        )
