from api.vendors.base import Base
from api.vendors.base import ResponseBase

class ApiAi(Base):
    def get_properties(self):
        properties = {}
        json = self.get_json()

        result = json.get('result', {})

        #Parameters
        #parameters['device_state'] = json['result']['parameters']['device_state']
        #parameters['light_type'] = json['result']['parameters']['light_type']
        #parameters['location'] = json['result']['parameters']['location']

        #Properties
        properties['action'] = result.get('action', "")
        properties['parameters'] = result.get("parameters", {})

        return properties


class ApiAiResponse(ResponseBase):
    def get_dict(self):
        return {
            "speech": self.speak_text,
            "displayText": self.display_text,
            "data": {},
            "contextOut": [],
            "source": "Yarvis"
        }
