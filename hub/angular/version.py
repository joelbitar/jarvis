__author__ = 'joel'

from django.conf import settings


def get_version():
    if not settings.AUTO_GENERATE_VERSION:
        return settings.VERSION

    import uuid
    return 'auto_' + str(uuid.uuid4())
