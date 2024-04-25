from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpRequest
from .models import Category, Product, Order, OrderItem
from userprofile.models import Userprofile
from .cart import Cart
from .forms import OrderForm
from .views import compare
from django.contrib.messages import get_messages


# Admin test cases
class AdminTestCase(TestCase):
    username = "adminTest"
    active_username = "activeUser"
    deactivated_username = "deactiveUser"
    seller_username = "testSeller"
    password = "testPassword"

    def setUp(self):
        admin = User.objects.create(username=self.username, is_staff=True)
        active_user = User.objects.create(username=self.active_username, is_active=True)
        deactivated_user = User.objects.create(username=self.deactivated_username, is_active=False)
        seller = User.objects.create(username=self.seller_username)
        seller_profile = Userprofile
        admin.set_password(self.password)
        admin.save()
        active_user.save()
        deactivated_user.save()
        seller.save()

        category = Category.objects.create(title="testCategory")
        category.save()
        product = Product.objects.create(user=seller, category=category, title="testBook", price=3099)
        product.save()

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

    def test_remove_listing(self):
        product = Product.objects.filter(title="testBook")[0]
        search_url = reverse('search')

        remove_listing_url = reverse('admin_unlist_item', kwargs={'product_id': product.id, 'from_path': search_url})
        self.client.post(remove_listing_url)

        try:
            Product.objects.get(title="testBook")
        except Product.DoesNotExist:
            pass
        else:
            self.fail("Book was not removed")


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

class CompareViewTestCase(TestCase):
    def setUp(self):
        # Create a category
        self.category = Category.objects.create(name='Test Category', slug='test-category')

        # Create original product
        self.original_product = Product.objects.create(
            name='Original Product',
            price=10.99,
            category=self.category
        )

        # Create similar products
        self.similar_product1 = Product.objects.create(
            name='Similar Product 1',
            price=12.99,
            category=self.category
        )

    def test_compare_view(self):
        request = HttpRequest()
        request.method = 'GET'

        response = compare(request, category_slug=self.category.slug, product_id=self.original_product.pk)

        self.assertEqual(response.status_code, 200)

        self.assertIn('original_product', response.context)

        self.assertIn('similar_products', response.context)

        self.assertTemplateUsed(response, 'inventory/compare.html')

class EditItemsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword!', is_staff=True)
        self.category = Category.objects.create(title='Test Category', slug='test-category')
        self.product = Product.objects.create(user=self.user, category=self.category, title='Edited Product title', slug='test-product', description='Edited Product Description', price=100)

    def test_click_username_seller_detail_page_access(self):
        seller_detail_url = reverse('seller_detail', kwargs={'pk': self.user.pk})
        response = self.client.get(seller_detail_url)
        self.assertEqual(response.status_code, 200)  #200 indicates successful access

    def test_order_detail_page_access(self):
        order = Order.objects.create(first_name=self.user, last_name=self.user)
        order_detail_url = reverse('my_items_order_detail', kwargs={'pk': order.pk})
        response = self.client.get(order_detail_url)
        self.assertEqual(response.status_code, 302)  #302 indicates successful access

    def test_edit_item_title(self):
        edit_item_url = reverse('edit_items', kwargs={'pk': self.product.pk})
        edited_data = {
            'title': 'Edited Product title',
            'price': 1500,
        }
        response = self.client.post(edit_item_url, edited_data)
        self.assertEqual(response.status_code, 302)  # 302 indicates successful redirect
        edited_product = Product.objects.get(pk=self.product.pk)

        self.assertEqual(edited_product.title, 'Edited Product title')

    def test_edit_item_description(self):
        edit_item_url = reverse('edit_items', kwargs={'pk': self.product.pk})
        edited_data = {
            'description': 'Edited Product Description',
        }
        response = self.client.post(edit_item_url, edited_data)

        self.assertEqual(response.status_code, 302)  # 302 indicates successful redirect
        edited_product = Product.objects.get(pk=self.product.pk)

        self.assertEqual(edited_product.description, 'Edited Product Description')

    def test_edit_item_price(self):
        edit_item_url = reverse('edit_items', kwargs={'pk': self.product.pk})
        edited_data = {
            'price': 100,
        }
        response = self.client.post(edit_item_url, edited_data)

        self.assertEqual(response.status_code, 302)  # 302 indicates successful redirect
        edited_product = Product.objects.get(pk=self.product.pk)

        self.assertEqual(edited_product.price, 100)
