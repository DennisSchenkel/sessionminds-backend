from django.utils import timezone
from datetime import timedelta
from rest_framework.test import APITestCase


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
        print(f"Access Token: {self.access_token}")
        print(f"Refresh Token: {self.refresh_token}")

    def test_token_lifespan(self):
        original_now = timezone.now
        timezone.now = lambda: original_now() + timedelta(minutes=1)

        # Refresh the token
        response = self.client.post(
            "/api/token/refresh/",
            {"refreshToken": self.refresh_token}
        )
        
        # Check if refresh token was returned successfully
        if "refreshToken" in response.data:
            new_refresh_token = response.data["refreshToken"]
            
            # Check if access token was returned successfully
            if "accessToken" in response.data:
                new_access_token = response.data["accessToken"]
                
                timezone.now = original_now
                
                self.client.credentials(
                    HTTP_AUTHORIZATION="Bearer " + new_access_token
                )
                response = self.client.get("/protected/")
                self.assertEqual(response.status_code, 200)

                response = self.client.post(
                    "/api/token/refresh/",
                    {"refreshToken": new_refresh_token}
                )
                
                # Check if access token was returned after refresh
                if "accessToken" in response.data:
                    new_access_token_after_refresh = response.data["accessToken"]
                    
                    self.client.credentials(
                        HTTP_AUTHORIZATION="Bearer " + new_access_token_after_refresh
                    )
                    response = self.client.get("/protected/")
                    self.assertEqual(response.status_code, 200)
            else:
                self.fail("Access token was not returned")
        else:
            self.fail("Refresh token was not returned")

    def test_access_with_valid_token(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token)
        response = self.client.get("/protected/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["message"],
            "You have access to this protected endpoint!"
            )

    def test_access_with_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + "invalidtoken")
        response = self.client.get("/protected/")
        self.assertEqual(response.status_code, 401)

    def test_access_with_expired_token(self):
        original_now = timezone.now
        timezone.now = lambda: original_now() + timedelta(minutes=2)

        response = self.client.post(
            "/api/token/refresh/",
            {"refreshToken": self.refresh_token}
        )
        
        # Check if refresh token was returned successfully
        if "refreshToken" in response.data:
            new_refresh_token = response.data["refreshToken"]
            
            # Refresh the token again
            response = self.client.post(
                "/api/token/refresh/",
                {"refreshToken": new_refresh_token}
            )
            
            if "accessToken" in response.data:
                new_access_token = response.data["accessToken"]
                
                timezone.now = original_now
                
                self.client.credentials(
                    HTTP_AUTHORIZATION="Bearer " + new_access_token
                )
                response = self.client.get("/protected/")
                self.assertEqual(response.status_code, 200)

                # Test expired token
                self.client.credentials(
                    HTTP_AUTHORIZATION="Bearer " + self.access_token
                )
                response = self.client.get("/protected/")
                self.assertEqual(response.status_code, 401)
        else:
            self.fail("Refresh token was not returned")
        

    def test_refresh_token_expired(self):
        original_now = timezone.now
        timezone.now = lambda: original_now() + timedelta(days=1)

        response = self.client.post(
            "/api/token/refresh/",
            {"refreshToken": self.refresh_token}
        )
        self.assertEqual(response.status_code, 401)

        timezone.now = original_now







class LogoutTest(APITestCase):
    def setUp(self):
        self.user_data = {
            "email": "testuser@example.com",
            "password": "testpass555515665161",
            "passwordConf": "testpass555515665161"
        }

        registration_response = self.client.post("/register/", self.user_data)
        self.assertEqual(registration_response.status_code, 201)

        login_response = self.client.post("/login/", {
            "email": self.user_data["email"],
            "password": self.user_data["password"]
        })
        self.assertEqual(login_response.status_code, 200)
        self.access_token = login_response.data["accessToken"]
        self.refresh_token = login_response.data["refreshToken"]

    def test_logout(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token
            )
        response = self.client.get("/protected/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["message"],
            "You have access to this protected endpoint!"
            )

        response = self.client.post(
            "/logout/", {"refresh_token": self.refresh_token}
            )
        self.assertEqual(response.status_code, 200)

        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token
            )
        response = self.client.get("/protected/")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.data["detail"], "Invalid token or token expired"
            )

        # Versuche, den Token zu erneuern, um zu bestätigen,
        # dass er ungültig ist
        response = self.client.post(
            "/api/token/refresh/", {"refreshToken": self.refresh_token}
            )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.data["detail"], "Token is blacklisted or invalid"
            )
