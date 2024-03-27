from django.db import models
from django.contrib.auth.models import User

class Userprofile(models.Model):
    USER = 'User'
    ADMIN = 'Admin'
    BUYER = 'Buyer'

    USER_STATUS = (
        (USER, 'User'),
        (ADMIN, 'Admin'),
        (BUYER, 'Buyer'),
    )

    user = models.OneToOneField(User, related_name='userprofile', on_delete=models.CASCADE)


    def __str__(self):
        return self.user.username