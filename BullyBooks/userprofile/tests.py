from django.test import TestCase
from django.contrib.auth.models import User
from .models import Userprofile
from django.urls import reverse
from django.utils.functional import lazy

# Create your tests here.
class LoginTestCase(TestCase):
    username = "loginTest"
    admin_username = "adminTest"
    buyer_username = "buyerTest"
    seller_username = "sellerTest"
    password = "testingLogin"

    def setUp(self):
        user = User.objects.create(username=self.username)
        admin = User.objects.create(username=self.admin_username, is_staff=True)
        buyer = User.objects.create(username=self.buyer_username)
        buyer_profile = Userprofile.objects.create(user=buyer, is_seller=False)
        seller = User.objects.create(username=self.seller_username)
        seller_profile = Userprofile.objects.create(user=seller, is_seller=True)
        user.set_password(self.password)
        admin.set_password(self.password)
        buyer.set_password(self.password)
        seller.set_password(self.password)
        user.save()
        admin.save()
        buyer.save()
        buyer_profile.save()
        seller.save()
        seller_profile.save()

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

    def test_buyer_login(self):
        login_url = reverse('login')
        login_data = {
            'username': self.buyer_username,
            'password': self.password
        }
        response = self.client.post(login_url, login_data)

        current_user = Userprofile.objects.get(user=response.wsgi_request.user)
        self.assertFalse(current_user.is_seller)

    def test_seller_login(self):
        login_url = reverse('login')
        login_data = {
            'username': self.seller_username,
            'password': self.password
        }
        response = self.client.post(login_url, login_data)

        current_user = Userprofile.objects.get(user=response.wsgi_request.user)
        self.assertTrue(current_user.is_seller)

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
