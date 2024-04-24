from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpRequest
from .models import Category, Product, Order, OrderItem
from .cart import Cart
from .forms import OrderForm

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

        activated_user = User.objects.filter(username=self.active_username)[0]
        self.assertFalse(activated_user.is_active)

    def test_access_database(self):
        database_url = reverse('admin:login')
        response = self.client.get(database_url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/admin/')

    def test_other_user_not_access_database(self):
        logout_url = reverse('logout')
        self.client.post(logout_url)

        database_url = reverse('admin:login')
        response = self.client.get(database_url)

        self.assertNotEqual(response.status_code, 302)        

class CartTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.category = Category.objects.create(title='Test Category', slug='test-category')
        self.product = Product.objects.create(user=self.user, category=self.category, title='Test Product', slug='test-product', description='Test description', price=100)
        self.cart_session = self.client.session
        self.cart_session.save()

    def test_remove_from_cart(self):
        request = HttpRequest()  # Create a request object
        request.session = self.cart_session  # Assign the session to the request
        cart = Cart(request)  # Pass the request object to the Cart class
        cart.add(str(self.product.id))  # Add product to cart
        cart.remove(str(self.product.id))  # Remove product from cart
        self.assertEqual(len(cart), 0)  # Cart should be empty after removing

    def test_add_to_cart(self):
        request = HttpRequest()  # Create a request object
        request.session = self.cart_session  # Assign the session to the request
        cart = Cart(request)  # Pass the request object to the Cart class
        cart.add(str(self.product.id))  # Use the product id as a string
        self.assertEqual(len(cart), 1)  # Cart should contain one item after adding

class OrderTestCase(TestCase):
    def test_order_creation(self):
        user = User.objects.create_user(username='testuser', password='password')
        form_data = {'first_name': 'John', 'last_name': 'Doe', 'address': '123 Street', 'city': 'City', 'state': 'State', 'zipcode': '12345'}
        form = OrderForm(data=form_data)
        self.assertTrue(form.is_valid())
        order = form.save(commit=False)
        order.created_by = user
        order.save()
        self.assertIsNotNone(order.id)
