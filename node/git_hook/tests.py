from django.conf import settings
from django.core.urlresolvers import reverse

from django.test import TestCase
from django.test import Client

from django.contrib.auth.models import User

# Create your tests here.
class GitHookAuthTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test',
            password='test'
        )

        client = Client()
        client.login(
            username='test',
            password='test'
        )

        self.client = client


    def test_should_get_not_auhtorized_when_posting_without_token(self):
        not_logged_in_client = Client()

        response = not_logged_in_client.post(
            reverse("git_hook")
        )

        self.assertEqual(
            response.status_code,
            403
        )

    def test_should_get_ok_when_posting_with_token(self):
        response = self.client.post(
            reverse("git_hook")
        )

        self.assertEqual(
            response.status_code,
            200
        )

