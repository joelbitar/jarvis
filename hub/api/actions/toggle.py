from api.actions.base import ActionBase
from device.command import Command


class ActionToggle(ActionBase):
    def run(self, properties):
        parameters = properties.get('parameters')

        command = Command()

        command.set_all_locations(
            parameters.get('location') == "all"
        )

        command.set_location_instance(
            self.get_location(parameters.get('location'))
        )
        command.set_light_type(
            self.get_light_type(parameters.get('light_type'))
        )

        if parameters.get('device_state') == 'on':
            command.turn_on()

        if parameters.get('device_state') == 'off':
            command.turn_off()

        response = self.get_response_object(
            speak_text = "Turned {new_state} {location} lights".format(
                new_state = parameters.get('device_state'),
                location = parameters.get('location')
            )
        )

        return response
