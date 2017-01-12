from api.actions.toggle import ActionToggle


class ActionRouter(object):
    def execute(self, properties):
        action = None
        if properties.get('action') == 'toggle':
            action = ActionToggle()

        action.run(properties)