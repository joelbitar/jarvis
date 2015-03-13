__author__ = 'joel'

from django.core.management.base import BaseCommand, CommandError

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class Command(BaseCommand):
    help = 'Executes commands..'

    def handle(self, *args, **options):
        for user in User.objects.all():
            try:
                auth_token = user.auth_token
            except Exception:
                auth_token = None

            if not auth_token:
                print('no auth token for {user.username} creating one.'.format(user=user))
                auth_token = Token.objects.create(user=user)

            print(user.username, ' ', auth_token.key)


