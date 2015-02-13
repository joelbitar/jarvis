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
        if command_name not in ['on', 'off', 'learn']:
            raise CommandError('command name "{command_name}" is not in white list'.format(command_name=command_name))

        if self.send_commands:
            call(['tdtool', '--' + command_name, str(self.device.pk)])
        else:
            print('Does not send command, in test mode.')

    def learn(self):
        self.execute_command('learn')

    def turn_on(self):
        self.execute_command('on')

    def turn_off(self):
        self.execute_command('off')
