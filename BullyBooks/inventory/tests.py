from django.test import TestCase
from django.urls import reverse
from django.http import HttpRequest
from django.contrib.auth.models import User
from .models import Category, Product, Order, OrderItem
from .cart import Cart
from .forms import OrderForm

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

    def test_cart_total_cost_calculation(self):
        # Add products to the cart
        request = HttpRequest()  # Create a request object
        request.session = self.cart_session  # Assign the session to the request
        cart = Cart(request)  # Pass the request object to the Cart class
        cart.add(str(self.product.id))  # Add product to cart
        total_cost = cart.cart_cost()  # Get the total cost from the cart
        expected_total_cost = self.product.price * 100  # Convert to cents
        self.assertEqual(total_cost, expected_total_cost)  # Check if total cost matches the expected value

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

class ViewTestCase(TestCase):
    def test_view_cart(self):
        response = self.client.get(reverse('view_cart'))
        self.assertEqual(response.status_code, 200)  # Should return success status
