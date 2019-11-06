from django.contrib import admin
from products.models import User, Product, Sprint

# Register your models here.
admin.site.register(User)
admin.site.register(Product)
admin.site.register(Sprint)
