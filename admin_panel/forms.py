from email.policy import default
from banner.models import Banner
from store.models import Product, CategoryOffer, ProductOffer
from category.models import Category
from django import forms
from django.core.validators import validate_image_file_extension,FileExtensionValidator
from django.forms.fields import DateField
from django.contrib.admin import widgets                
from cart.models import Coupon                       

class ProductForm(forms.ModelForm):
    is_available    = forms.BooleanField(required=False, initial=True)
    product_img_0   = forms.ImageField(validators=[validate_image_file_extension])
    product_img_1   = forms.ImageField(validators=[validate_image_file_extension])
    product_img_2   = forms.ImageField(validators=[validate_image_file_extension])
    product_img_3   = forms.ImageField(validators=[validate_image_file_extension])
    description     = forms.Textarea()
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class CategoryForm(forms.ModelForm):
    category_img    = forms.ImageField( validators=[validate_image_file_extension])
    class Meta:
        model = Category
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class BannerForm(forms.ModelForm):
    image       = forms.ImageField( validators=[validate_image_file_extension])
    class Meta:
        model = Banner
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(BannerForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class CategoryOfferForm(forms.ModelForm):
    valid_from    = forms.DateField(widget=forms.DateInput(attrs=dict(type='date')))
    valid_to      = forms.DateField(widget=forms.DateInput(attrs=dict(type='date')))
    class Meta:
        model = CategoryOffer
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CategoryOfferForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class ProductOfferForm(forms.ModelForm):
    valid_from    = forms.DateField(widget=forms.DateInput(attrs=dict(type='date')))
    valid_to      = forms.DateField(widget=forms.DateInput(attrs=dict(type='date')))
    class Meta:
        model = ProductOffer
        fields = '__all__'

        

    def __init__(self, *args, **kwargs):
        super(ProductOfferForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class CouponForm(forms.ModelForm):
    valid_from    = forms.DateField(widget=forms.DateInput(attrs=dict(type='date')))
    valid_to      = forms.DateField(widget=forms.DateInput(attrs=dict(type='date')))
    class Meta:
        model = Coupon
        fields = '__all__'
        

    def __init__(self, *args, **kwargs):
        super(CouponForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'



