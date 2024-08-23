from django.utils import timezone
from datetime import timedelta
from rest_framework.test import APITestCase


class JWTTokenTest(APITestCase):
    def setUp(self):
        self.user_data = {
            'email': 'testuser@example.com',
            'password': 'testpass555515665161',
            'passwordConf': 'testpass555515665161'
        }
        # Create a user
        registration_response = self.client.post('/register/', self.user_data)
        print(registration_response.data)
        self.assertEqual(registration_response.status_code, 201)

    def test_token_lifespan(self):
        # Log in and get tokens
        response = self.client.post('/login/', {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        })
        print(response.data)
        self.assertEqual(response.status_code, 200)
        refresh_token = response.data['refresh']

        # Simulate token expiration by advancing time
        original_now = timezone.now
        timezone.now = (
            lambda: original_now() +
            timedelta(minutes=6)
            )  # forward time

        # Try to refresh the token
        response = self.client.post(
            '/api/token/refresh/',
            {'refresh': refresh_token}
            )
        self.assertEqual(response.status_code, 200)

        # Reset the time
        timezone.now = original_now
