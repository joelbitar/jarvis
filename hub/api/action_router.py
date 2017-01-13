from api.actions.toggle import ActionToggle
from api.actions.temperature import GetTemperature


class ActionRouter(object):
    __vendor_name = None

    def set_vendor_name(self, vendor_name):
        self.__vendor_name = vendor_name

    @property
    def vendor_name(self):
        return self.__vendor_name

    def get_action(self, properties):
        action_name = properties.get('action')
        if action_name == 'toggle':
            return ActionToggle(vendor_name=self.vendor_name)

        if action_name == 'get_temperature':
            return GetTemperature(vendor_name=self.vendor_name)

        return None

    def execute(self, properties):
        action = self.get_action(properties)
        return action.run(properties)