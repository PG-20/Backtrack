from django.contrib import admin
from .models import CustomUser, Product

admin.site.register(Product)
admin.site.register(CustomUser)



