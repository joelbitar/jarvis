__author__ = 'joel'
import string
import math

from django.db.models import Max

from device.models import Device


class PropertyConf(object):
    __conf = None

    def __init__(self, conf):
        self.__conf = conf

    @property
    def type(self):
        return self.__conf['type']

    @property
    def name(self):
        return self.__conf['name']

    @property
    def min(self):
        return self.__conf['min']

    @property
    def max(self):
        return self.__conf['max']

    def __str__(self):
        return self.__conf

    def __unicode__(self):
        return self.__str__()


class PropertyValueGenerator(object):
    TYPE_CHARACTER = 1
    TYPE_INTEGER = 2

    __iteration = 0
    __start_point = None
    __config = None

    def __init__(self, *args, iteration=None):
        self.reset()
        if iteration is not None:
            self.__iteration = iteration

        self.__config = [PropertyConf(c) for c in args]

    @property
    def config(self):
        return self.__config

    @property
    def iteration(self):
        return self.__iteration

    def get_property_conf(self, property_name):
        for property_conf in self.config:
            if property_conf.name == property_name:
                return property_conf

        return None

    def generate_character(self):
        pass

    def get_possibilities_count(self, conf):
        if conf.type == self.TYPE_INTEGER:
            c = conf.max - conf.min
            return c + 1

        if conf.type == self.TYPE_CHARACTER:
            letters = string.ascii_lowercase
            c = letters.find(conf.max) - letters.find(conf.min)
            return c + 1

    def get_total_possibilities_count(self):
        total_possibilities_count = 1

        for conf in self.config:
            total_possibilities_count *= self.get_possibilities_count(conf)

        return total_possibilities_count

    def pick_value(self, conf, pick_at):
        if conf.type == self.TYPE_CHARACTER:
            pick_at += string.ascii_lowercase.find(conf.min)
            return string.ascii_uppercase[pick_at]

        if conf.type == self.TYPE_INTEGER:
            # just add minimum value.
            return pick_at + conf.min

    def generate_output(self):
        output = {}

        j = self.iteration

        for conf in self.config:
            possibilities_count = self.get_possibilities_count(conf=conf)

            # Where to pick value for THIS current conf
            pick_value_at = j % possibilities_count

            # How much is left
            j = math.floor(j / possibilities_count)

            # Add to output array
            output[conf.name] = self.pick_value(conf=conf, pick_at=pick_value_at)

        return output

    def reset(self):
        self.reset_iteration()
        self.__config = None

    def reset_iteration(self):
        self.set_iteration(0)

    def set_iteration(self, iteration):
        self.__iteration = iteration

    def __call__(self, *args, **kwargs):
        # If the comming iteration is Larger (or equal) we can NOT generate another number
        if self.get_total_possibilities_count() <= self.__iteration:
            raise ValueError('Max Value Reached')

        output = self.generate_output()
        self.__iteration += 1
        return output


class DevicePropertyGenerator(object):
    __device = None

    def __init__(self, device):
        self.__device = device

    @property
    def device(self):
        return self.__device

    def get_protocol_model_generator_map(self):
        arctec_codeswitch = (
            Device.PROTOCOL_ARCHTEC, Device.MODEL_CODESWITCH, PropertyValueGenerator(
                {
                    'name': 'unit',
                    'type': PropertyValueGenerator.TYPE_INTEGER,
                    'min': 1,
                    'max': 16
                },
                {
                    'name': 'house',
                    'type': PropertyValueGenerator.TYPE_CHARACTER,
                    'min': 'a',
                    'max': 'p'
                },
            )
        )

        return (
            arctec_codeswitch,
        )

    def get_max_property_iteration(self):
        # Gets max 'property_iteration' within the PROTOCOL and MODEL group ov devices
        return Device.objects.filter(
            model=self.device.model,
            protocol=self.device.protocol
        ).aggregate(Max('property_iteration'))['property_iteration__max']

    def get_property_value_generator(self):
        for protocol, model, property_value_generator_instance in self.get_protocol_model_generator_map():
            if self.device.protocol == protocol and self.device.model == model:
                return property_value_generator_instance

        return None

    def is_device_unique(self, device, properties):
        kwargs = {
            'model': device.model,
            'protocol': device.protocol
        }
        kwargs.update(
            properties
        )

        return not Device.objects.filter(
            **kwargs
        ).exists()

    def generate_properties(self, save_model=False):
        property_value_generator = self.get_property_value_generator()

        # set the current iteration, if None is returned (this is the first) set 1
        property_value_generator.set_iteration(
            iteration=self.get_max_property_iteration() or 0
        )

        while True:
            properties = property_value_generator()

            if not self.is_device_unique(self.device, properties):
                continue


            for key, value in properties.items():
                setattr(self.device, key, value)

            self.device.property_iteration = property_value_generator.iteration
            self.device.save()

            break

        return self.device, property_value_generator.iteration










