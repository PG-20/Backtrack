from django.db import models

from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    name = models.CharField('name', max_length=150)
    email = models.EmailField('email address', unique=True)
    developing = models.ForeignKey('Product', on_delete=models.SET_NULL, related_name='developers', default=None,
                                   null=True, blank=True)
    role = models.PositiveSmallIntegerField(choices=[(1, 'Developer'), (2, 'Manager')], default=1)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.name


class Product(models.Model):
    owner = models.OneToOneField(CustomUser, on_delete=models.PROTECT, related_name='productOwned')
    name = models.CharField(max_length=30)
    created_at = models.DateField(auto_now_add=True)
    sprint_length = models.PositiveSmallIntegerField(default=15)

    def __str__(self):
        return self.name
