from django.db.models.signals import pre_save
from django.dispatch import receiver
from device.models import Device
from device.property_generator import DevicePropertyGenerator

@receiver(pre_save, sender=Device)
def my_handler(sender, instance, **kwargs):
    if instance.pk != None:
        return None

    device_property_generator = DevicePropertyGenerator(device=instance)
    properties, iteration = device_property_generator.generate_properties()

    
