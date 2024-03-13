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
    added_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-added_date', )

    def __str__(self):
        return self.title

    def get_display_price(self):
        return self.price / 100
        