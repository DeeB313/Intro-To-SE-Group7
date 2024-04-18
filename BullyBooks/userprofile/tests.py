from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

# Create your tests here.
class LoginTestCase(TestCase):
    username = "loginTest"
    admin_username = "adminTest"
    password = "testingLogin"

    def setUp(self):
        user = User.objects.create(username=self.username)
        admin = User.objects.create(username=self.admin_username, is_staff=True)
        user.set_password(self.password)
        admin.set_password(self.password)
        user.save()
        admin.save()

    def test_universal_user_login(self):
        login_url = reverse('login')
        login_data = {
            'username': self.username,
            'password': self.password,
        }
        response = self.client.post(login_url, login_data)

        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_admin_login(self):
        login_url = reverse('login')
        login_data = {
            'username': self.admin_username,
            'password': self.password,
        }
        response = self.client.post(login_url, login_data)

        self.assertTrue(response.wsgi_request.user.is_staff)

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
