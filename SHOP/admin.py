from django.contrib import admin
from .models import Products
from .models import Customer
from .models import Tag
from .models import Product
from .models import Order
# Register your models here.


admin.site.register(Products)
admin.site.register(Customer)
admin.site.register(Tag)
admin.site.register(Product)
admin.site.register(Order)