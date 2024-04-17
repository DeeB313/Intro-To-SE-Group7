from django.db import models
from django.contrib.auth.models import User

class Userprofile(models.Model):
    user = models.OneToOneField(User, related_name='userprofile', on_delete=models.CASCADE)
    is_seller = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.user.username} - {'Seller' if self.is_seller else 'Buyer'}"