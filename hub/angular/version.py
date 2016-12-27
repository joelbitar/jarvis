__author__ = 'joel'

from django.conf import settings


def get_version(real_version=False):
    if not settings.AUTO_GENERATE_VERSION or real_version:
        return settings.VERSION

    import uuid
    return 'auto_' + str(uuid.uuid4())
