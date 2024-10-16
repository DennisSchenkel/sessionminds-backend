from django.utils import timezone
from datetime import timedelta
from rest_framework.test import APITestCase
from freezegun import freeze_time


class JWTTokenTest(APITestCase):
    def setUp(self):
        # Test data for a user
        self.user_data = {
            "email": "testuser@example.com",
            "password": "testpass555515665161",
            "passwordConf": "testpass555515665161"
        }
        # Create user
        registration_response = self.client.post("/register/", self.user_data)
        self.assertEqual(registration_response.status_code, 201)

        # Login of user
        login_response = self.client.post("/login/", {
            "email": self.user_data["email"],
            "password": self.user_data["password"]
        })
        self.assertEqual(login_response.status_code, 200)
        self.access_token = login_response.data["accessToken"]
        self.refresh_token = login_response.data["refreshToken"]
        print("Token Test User created and logged in")
        print(" Access Token: ", {self.access_token})
        print(" Refresh Token: ", {self.refresh_token})

    def test_token_lifespan(self):
        original_now = timezone.now
        timezone.now = lambda: original_now() + timedelta(minutes=1)

        # Refresh the token
        response = self.client.post(
            "/api/token/refresh/",
            {"refresh": self.refresh_token}
        )

        # Check if refresh token was returned successfully
        if "refresh" in response.data:
            new_refresh_token = response.data["refresh"]

            # Check if access token was returned successfully
            if "access" in response.data:
                new_access_token = response.data["access"]

                timezone.now = original_now

                self.client.credentials(
                    HTTP_AUTHORIZATION="Bearer " + new_access_token
                )
                response = self.client.get("/protected/")
                self.assertEqual(response.status_code, 200)

                response = self.client.post(
                    "/api/token/refresh/",
                    {"refresh": new_refresh_token}
                )

                # Check if access token was returned after refresh
                if "access" in response.data:
                    new_access_token_after_refresh = response.data["access"]

                    self.client.credentials(
                        HTTP_AUTHORIZATION="Bearer "
                        + new_access_token_after_refresh
                    )
                    response = self.client.get("/protected/")
                    self.assertEqual(response.status_code, 200)
                    print("Token lifespan test passed")
            else:
                self.fail("Access token was not returned")
        else:
            self.fail("Refresh token was not returned")

    def test_access_with_valid_token(self):
        print("\n Test access with valid token")
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token)
        response = self.client.get("/protected/")
        self.assertEqual(response.status_code, 200)
        print("Response in test with valid token = ", response.content)

    def test_access_with_invalid_token(self):
        print("\n Test access with invalid token")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + "invalidtoken")
        response = self.client.get("/protected/")
        self.assertEqual(response.status_code, 401)
        print("Response in test with invalid token = ", response.content)

    def test_access_with_expired_token(self):
        with freeze_time(timezone.now() + timedelta(minutes=10)):
            print("\n Test access with expired token")

            response = self.client.post(
                "/api/token/refresh/", {"refresh": self.refresh_token}
                )
            print(
                "Response in test with invalid token = ",
                response.content, "Status code = ", response.status_code
                )

            new_access_token = response.data["access"]
            print(" New_access token = ", new_access_token)
            print(" Old access token = ", self.access_token)

            self.client.credentials(
                HTTP_AUTHORIZATION="Bearer " + new_access_token
                )

            response = self.client.get("/protected/")
            self.assertEqual(response.status_code, 200)
            print(
                "Response in test with expired access token = ",
                response.content
                )

            self.client.credentials(
                HTTP_AUTHORIZATION="Bearer " + self.access_token
                )

            response = self.client.get("/protected/")
            self.assertEqual(response.status_code, 401)
            print(
                "Response in test with expired access token = ",
                response.content
                )

    def test_refresh_token_expired(self):
        print("\n Test refresh token expired")
        with freeze_time(timezone.now() + timedelta(days=1)):
            response = self.client.post(
                "/api/token/refresh/",
                {"refresh": self.refresh_token}
            )
            self.assertEqual(response.status_code, 401)
            print(
                "Response in test with expired refresh token = ",
                response.content
                )

    def test_logout(self):
        print("\n Test logout")
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token
            )
        response = self.client.get("/protected/")
        self.assertEqual(response.status_code, 200)
        print("Response in test with valid token = ", response.content)

        response = self.client.post(
            "/logout/",
            {"refreshToken": self.refresh_token,
             "accessToken": self.access_token}
            )
        self.assertEqual(response.status_code, 200)
        print("Response in test with logout = ", response.content)

        with freeze_time(timezone.now() + timedelta(minutes=10)):
            self.client.credentials(
                HTTP_AUTHORIZATION="Bearer " + self.access_token
                )
            response = self.client.get("/protected/")
            self.assertEqual(response.status_code, 401)
            print("Response in test with expired token = ", response.content)

            response = self.client.post(
                "/api/token/refresh/", {"refresh": self.refresh_token}
                )
            self.assertEqual(response.status_code, 401)
            print(
                "Response in token refresh with blacklisted refresh token = ",
                response.content
                )
