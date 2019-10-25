from django.db import models

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=30, blank=False)
    email = models.CharField(max_length=30)
    password = models.CharField(max_length=16)

    def __str__(self):
        return self.name


class Product(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    created_at = models.DateField()

    def __str__(self):
        return self.name