from dataclasses import fields
from .models import Order
from django import forms
from django.contrib.auth.forms import UserChangeForm
from accounts.models import Address

class OrderForm(forms.ModelForm):
    class Meta:
        model   = Order
        fields  = ['first_name', 'last_name', 'email', 'phone_number', 'address_line_1', 'address_line_2', 'country', 'state', 'city', 'pin' ,'order_note']
            
class UserAddressForm(forms.ModelForm):
    class Meta:
        model   = Address
        exclude = ('user',)


    def __init__(self, *args, **kwargs):
        super(UserAddressForm, self).__init__(*args, **kwargs)

        for field in self.fields:
              self.fields[field].widget.attrs['class'] = 'form-control'
    
    
  