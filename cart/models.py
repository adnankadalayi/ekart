from django.db import models
from store.models import Product
from accounts.models import Accounts, Address
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    user        = models.ForeignKey(Accounts, on_delete=models.CASCADE, null=True)
    product     = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart        = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    address     = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    price       = models.IntegerField(null=True)  
    quantity    = models.IntegerField()
    is_active   = models.BooleanField(default=True)

    def __str__(self):
        return str(self.product)

    def sub_total(self):
        return self.product.price * self.quantity

class Coupon(models.Model):
    code = models.CharField(max_length=15, unique=True)
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    is_active = models.BooleanField()


    def __str__(self):
        return self.code