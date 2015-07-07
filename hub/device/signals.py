from django.core import mail

from django.db.models.signals import pre_save
from django.db.models.signals import post_save
from django.dispatch import receiver
from device.models import Device

from device.property_generator import DevicePropertyGenerator

@receiver(pre_save, sender=Device)
def my_handler(sender, instance, **kwargs):
    # If the instnace is an old one.
    if instance.pk != None:
        return None

    device_property_generator = DevicePropertyGenerator(device=instance)
    properties, iteration = device_property_generator.generate_properties()

@receiver(pre_save, sender=Device)
def reset_written_to_conf_on_node(sender, instance, **kwargs):
    # If the instnace is an old one.
    if instance.pk is None:
        return None

    if instance.node is None:
        return None

    try:
        old_device = Device.objects.get(pk=instance.pk)
    except Device.DoesNotExist:
        # There was no old device, this can happen when we load fixtures for instance
        return None

    if old_device.node != instance.node:
        instance.written_to_conf_on_node = False
        instance.learnt_on_node = False

@receiver(post_save, sender=Device)
def send_to_node(sender, instance, **kwargs):
    if hasattr(mail, 'outbox'):
        return None

    if instance.node_device_pk is not None:
        return None

    node_device_communicator = instance.get_communicator() 
    node_device_communicator.create()


