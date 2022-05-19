from telnetlib import STATUS
from django.db import models
from accounts. models import Accounts, Address
from store.models import Product
import datetime
from cart.models import Coupon
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.


class Payment(models.Model):
    user            = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    payment_id      = models.CharField(max_length=50)
    payment_method  = models.CharField(max_length=50)
    amount_paid     = models.CharField(max_length=50)
    status          = models.CharField(max_length=50)
    created_at      = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id

class Order(models.Model):
    STATUS = (
        ('Ordered', 'Ordered'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Returned', 'Returned'),
        ('Cancelled', 'Cancelled')
    )

    user            = models.ForeignKey(Accounts, on_delete=models.SET_NULL, null=True, blank=True)
    payment         = models.ForeignKey(Payment, on_delete=models.SET_NULL, null= True)
    order_number    = models.CharField(max_length=20, null=True)
    first_name      = models.CharField(max_length=50, null=True)
    last_name       = models.CharField(max_length=50, null=True)
    phone_number    = models.CharField(max_length=10, null=True)
    email           = models.EmailField(max_length=50, null=True)
    address_line_1  = models.CharField(max_length=50, null=True)
    address_line_2  = models.CharField(max_length=50, blank=True, null=True)
    country         = models.CharField(max_length=50, null=True)
    state           = models.CharField(max_length=50, null=True)
    city            = models.CharField(max_length=50, null=True)
    pin             = models.IntegerField(null=True)
    order_note      = models.CharField(max_length=100, blank=True, null=True)
    order_total     = models.FloatField(null=True)
    tax             = models.FloatField(null=True)
    status          = models.CharField(max_length=20, choices=STATUS, default='Ordered', null=True)
    is_ordered      = models.BooleanField(default=False, null=True)
    created_at      = models.DateTimeField(auto_now_add=True, null=True)
    modified_at     = models.DateTimeField(auto_now=True, null=True)
    tracking_no     = models.CharField(max_length=150, null=True)
    coupon          = models.ForeignKey(Coupon, related_name="orders", on_delete= models.SET_NULL,blank=True, null=True )  
    discount        = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)], null=True)
    

    def __str__(self):
        return str(self.first_name)              

    def full_name(self):                                                       
        return f'{self.first_name}{self.last_name}'

    def full_address(self):
        return f'{self.address_line_1}{self.address_line_2}'
        
class OrderProduct(models.Model):
    user            = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    payment         = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    order           = models.ForeignKey(Order, on_delete=models.CASCADE)
    product         = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity        = models.IntegerField()
    # here not null in price
    product_price   = models.FloatField(null=True)
    ordered         = models.BooleanField(default=False)
    created_at      = models.DateTimeField(auto_now_add=True)
    modified_at     = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.product.product_name)
