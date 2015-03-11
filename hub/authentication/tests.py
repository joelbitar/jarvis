from django.test import TestCase
from django.contrib.auth.models import User
from django.test.client import Client
from django.core.urlresolvers import reverse

import json


# Create your tests here.
class UserAPITests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test',
            password='test',
            email='test@example.com'
        )

    def test_get_logged_in_user_should_yield_empty_response_for_not_logged_in_client(self):
        c = Client()
        r = c.get(
            reverse('current-user')
        )

        self.assertEqual(
            r.status_code,
            200
        )

        self.assertEqual(
            r.content.decode('utf-8'),
            '{}'
        )

    def test_get_logged_in_user_should_yield_serialized_user_for_logged_in_client(self):
        c = Client()
        c.login(
            username='test',
            password='test'
        )

        r = c.get(
            reverse('current-user')
        )

        self.assertEqual(
            r.status_code,
            200
        )

        self.assertJSONEqual(
            r.content.decode('utf-8'),
            json.dumps(
                {
                    'pk': self.user.pk,
                    'first_name': self.user.first_name,
                    'last_name': self.user.last_name,
                    'auth_token': self.user.auth_token.key,
                }
            )
        )

    def test_should_be_able_to_login_with_ajax_api(self):
        c = Client()

        r = c.post(
            reverse('login'),
            data=json.dumps({
                'username': 'test',
                'password': 'test'
            }),
            content_type='application/json'
        )

        self.assertEqual(
            r.status_code,
            200
        )

        self.assertIn('_auth_user_id', c.session)
        self.assertEqual(int(c.session['_auth_user_id']), self.user.pk)

    def test_should_not_be_able_to_login_with_ajax_api_with_wrong_credentials(self):
        c = Client()

        r = c.post(
            reverse('login'),
            data=json.dumps({
                'username': 'test',
                'password': 'apa'
            }),
            content_type='application/json'
        )

        self.assertEqual(
            r.status_code,
            403
        )

    def test_logout_with_api(self):
        c = Client()
        c.login(
            username='test',
            password='test'
        )

        r = c.post(
            reverse('logout'),
            data=json.dumps({}),
            content_type='application/json'
        )

        self.assertEqual(
            r.status_code,
            200
        )

        self.assertNotIn('_auth_user_id', c.session)

    def test_should_be_able_to_authenticate_with_tokens(self):
        c = Client(
            HTTP_AUTHORIZATION='Token ' + self.user.auth_token.key
        )

        r = c.get(
            reverse('device-list'),
        )

        self.assertEqual(
            r.status_code,
            200
        )

    def test_should_not_be_able_to_get_without_tokens(self):
        c = Client()

        r = c.get(
            reverse('device-list')
        )

        self.assertEqual(
            r.status_code,
            403
        )