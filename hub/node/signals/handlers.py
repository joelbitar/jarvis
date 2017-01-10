__author__ = 'joel'

# Imprted in node __init__.py

from github_hook.models import hook_signal


def processWebhook(sender, **kwargs):
    print('Process Webhook')

    for key, value in kwargs.items():
        print(key, value)


hook_signal.connect(processWebhook)
