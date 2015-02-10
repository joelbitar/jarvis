__author__ = 'joel'
import os
from subprocess import call


class CommandDispatcher(object):
    __device = None

    def __init__(self, device):
        self.__device = device

    @property
    def device(self):
        return self.__device

    def execute_command(self, command_name):
        call(['tdtool', command_name, str(self.device.pk)])

    def learn(self):
        self.execute_command('--learn')

    def turn_on(self):
        self.execute_command('--on')

    def turn_off(self):
        self.execute_command('--off')
