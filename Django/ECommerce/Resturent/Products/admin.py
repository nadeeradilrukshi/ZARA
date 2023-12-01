from django.contrib import admin
from . import models
from .models import CartItem

admin.site.register(CartItem)
# Register your models here.

admin.site.register(models.Product) 
#admin.site.register(models.CartItem)