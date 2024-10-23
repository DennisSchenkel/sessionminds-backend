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
        self.access_token = login_response.data["access"]
        self.refresh_token = login_response.data["refresh"]

    # Test token lifespan
    def test_1_token_lifespan(self):
        print("\nProfile Test 1: Token lifespan")
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
                    print("Test passed \n")
            else:
                self.fail("Access token was not returned")
        else:
            self.fail("Refresh token was not returned")

    # Test access with valid access token
    def test_2_access_with_valid_token(self):
        print("\nProfile Test 2: Access with valid token")
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token)
        response = self.client.get("/protected/")
        self.assertEqual(response.status_code, 200)
        print("Test passed \n")

    # Test access with invalid access token
    def test_3_access_with_invalid_token(self):
        print("\nProfile Test 3: Access with invalid token")
        # Add invalid token to the request header instead of the valid token
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + "invalidtoken")
        response = self.client.get("/protected/")
        self.assertEqual(response.status_code, 401)
        print("Test passed \n")

    # Test access with expired token
    def test_4_access_with_expired_token(self):
        print("\nProfile Test 4: Access with expired token")
        self.client.credentials(
                HTTP_AUTHORIZATION="Bearer " + self.access_token
                )
        response = self.client.get("/protected/")
        self.assertEqual(response.status_code, 200)
        print("Test passed")
        with freeze_time(timezone.now() + timedelta(minutes=20)):
            # Test access with expired access token
            response = self.client.post(
                "/api/token/refresh/", {"refresh": self.refresh_token}
                )
            new_access_token = response.data["access"]
            self.client.credentials(
                HTTP_AUTHORIZATION="Bearer " + new_access_token
                )
            response = self.client.get("/protected/")
            self.assertEqual(response.status_code, 200)
            print("Test passed")

            self.client.credentials(
                HTTP_AUTHORIZATION="Bearer " + self.access_token
                )
            response = self.client.get("/protected/")
            self.assertEqual(response.status_code, 401)
            print("Test passed \n")

    # Test refreshing access token with expired refresh token
    def test_5_refresh_token_expired(self):
        print("\nProfile Test 5: Refresh token expired")
        with freeze_time(timezone.now() + timedelta(days=2)):
            response = self.client.post(
                "/api/token/refresh/",
                {"refresh": self.refresh_token}
            )
            self.assertEqual(response.status_code, 401)
            print("Test passed \n")

    # Test access with valid token
    def test_6_logout(self):
        print("\nProfile Test 6: Logout")
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token
            )
        response = self.client.get("/protected/")
        self.assertEqual(response.status_code, 200)
        print("Test passed")

        # Conduct logout and blacklist the refresh token
        logout_response = self.client.post(
            "/logout/",
            {"refreshToken": self.refresh_token}
            )
        self.assertEqual(logout_response.status_code, 200)
        print("Test passed")

        # Test access with blacklisted token
        response = self.client.post(
            "/api/token/refresh/", {"refresh": self.refresh_token}
            )
        self.assertEqual(response.status_code, 401)
        print("Test passed")

        # Test access with valid access token after logout
        response = self.client.get("/protected/")
        self.assertEqual(response.status_code, 200)
        print("Test passed")

        with freeze_time(timezone.now() + timedelta(minutes=20)):
            # Test access with expired access token after logout
            self.client.credentials(
                HTTP_AUTHORIZATION="Bearer " + self.access_token
                )
            response = self.client.get("/protected/")
            self.assertEqual(response.status_code, 401)
            print("Test passed")

            # Test refreshing access token with expired refresh token
            response = self.client.post(
                "/api/token/refresh/", {"refresh": self.refresh_token}
                )
            self.assertEqual(response.status_code, 401)
            print("Test passed \n")
