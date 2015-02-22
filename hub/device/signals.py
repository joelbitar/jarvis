from django.core import mail

from django.db.models.signals import pre_save
from django.db.models.signals import post_save
from django.dispatch import receiver
from device.models import Device

from device.property_generator import DevicePropertyGenerator

@receiver(pre_save, sender=Device)
def my_handler(sender, instance, **kwargs):
    if instance.pk != None:
        return None

    device_property_generator = DevicePropertyGenerator(device=instance)
    properties, iteration = device_property_generator.generate_properties()

@receiver(post_save, sender=Device)
def send_to_node(sender, instance, **kwargs):
    if hasattr(mail, 'outbox'):
        return None

    if instance.node_device_pk is not None:
        return None

    node_device_communicator = instance.get_communicator() 
    node_device_communicator.create()


