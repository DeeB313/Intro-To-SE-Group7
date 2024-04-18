from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

# Admin test cases
class AdminTestCase(TestCase):
    username = "adminTest"
    active_username = "activeUser"
    deactivated_username = "deactiveUser"
    password = "adminLogin"

    def setUp(self):
        admin = User.objects.create(username=self.username, is_staff=True)
        active_user = User.objects.create(username=self.active_username, is_active=True)
        deactivated_user = User.objects.create(username=self.deactivated_username, is_active=False)
        admin.set_password(self.password)
        admin.save()
        active_user.save()
        deactivated_user.save()
        login_url = reverse('login')
        login_data = {
            'username': self.username,
            'password': self.password,
        }
        self.client.post(login_url, login_data)

    def test_activate_user(self):
        change_url = reverse('change_status', kwargs={'username': self.deactivated_username}) + "?action=activate"
        self.client.post(change_url)

        deactivated_user = User.objects.filter(username=self.deactivated_username)[0]
        self.assertTrue(deactivated_user.is_active)

    def test_deactivate_user(self):
        change_url = reverse('change_status', kwargs={'username': self.active_username}) + "?action=deactivate"
        self.client.post(change_url)

        active_user = User.objects.filter(username=self.active_username)[0]
        self.assertFalse(active_user.is_active)
