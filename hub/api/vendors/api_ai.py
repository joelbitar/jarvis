from api.vendors.base import Base


class ApiAi(Base):
    def get_properties(self):
        parameters = {}
        properties = {}
        json = self.get_json()

        #Parameters
        parameters['device_state'] = json['result']['parameters']['device_state']
        parameters['light_type'] = json['result']['parameters']['light_type']
        parameters['location'] = json['result']['parameters']['location']

        #Properties
        properties['action'] = json['result']['action']
        properties['parameters'] = parameters

        return properties


