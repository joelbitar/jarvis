from api.actions.base import ActionBase
from device.command import Command

from api.vendors.api_ai import ApiAiResponse

from django.db.models import Avg


class GetTemperature(ActionBase):
    def get_sensors(self, location_slug):
        location = self.get_location(
           slug=location_slug
        )

        return location.sensors.all()

    def get_temperature(self, sensors):
        result = sensors.aggregate(Avg('temperature'))

        return result.get('temperature__avg', None)

    def run(self, properties):
        parameters = properties.get('parameters')

        sensors = self.get_sensors(
            location_slug=parameters.get('location')
        )

        temperature = self.get_temperature(sensors=sensors)

        response = self.get_response_object(
            speak_text = "It is {temperature:.1f} degrees".format(
                temperature=temperature
            )
        )

        return response
