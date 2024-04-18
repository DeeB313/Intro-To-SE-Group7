from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

# Create your tests here.
class LoginTestCase(TestCase):
    username = "loginTest"
    password = "testingLogin"

    def setUp(self):
        user = User.objects.create(username=self.username)
        user.set_password(self.password)
        user.save()

    def test_universal_user_login(self):
        login_url = reverse('login')
        login_data = {
            'username': self.username,
            'password': self.password,
        }
        response = self.client.post(login_url, login_data)

        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_invalid_user_login(self):
        login_url = reverse('login')
        login_data = {
            'username': "invalid",
            'password': "invalid",
        }
        response = self.client.post(login_url, login_data)

        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_user_logout(self):
        login_url = reverse('login')
        login_data = {
            'username': self.username,
            'password': self.password,
        }
        self.client.post(login_url, login_data)

        logout_url = reverse('logout')
        response = self.client.post(logout_url)

        self.assertFalse(response.wsgi_request.user.is_authenticated)
