from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    title = models.CharField(max_length=70)
    slug = models.SlugField(max_length=70)


    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title
    
class Product(models.Model):
    user = models.ForeignKey(User, related_name='products', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    title = models.CharField(max_length=70)
    slug = models.SlugField(max_length=70)
    description = models.TextField(blank=True)
    price = models.IntegerField()
    image = models.ImageField(upload_to='uploads/product_images/', blank=True, null=True)
    added_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-added_date', )

    def __str__(self):
        return self.title

    def get_display_price(self):
        return self.price / 100
    
    def add_to_cart(self, request):
        cart = Cart.objects.get(user=request.user)
        CartItem.objects.create(cart=cart, product=self)
        cart.total += self.price

class Cart(models.Model):
    id = models.CharField(primary_key=True, max_length=9)
    total = models.DecimalField(decimal_places=2, max_digits=9)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username}: {self.product.title}'
        