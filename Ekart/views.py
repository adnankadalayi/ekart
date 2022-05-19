from django.shortcuts import render
from store.models import Product, CategoryOffer
from category.models import Category
from banner.models import Banner
from cart.models import Cart 
from accounts.models import Referral 

def home(request, *args, **kwargs):

    products = Product.objects.all().filter(is_available=True, is_trending=True)
    category = Category.objects.all()
    banners  = Banner.objects.all().order_by('id')
   
    code = str(kwargs.get('ref_code'))
    try:
        profile = Referral.objects.get(code=code)
        request.session['ref_profile'] = profile.id
    except:
        pass

    context = { 
        'products' :products,
        'banners' : banners,
        'category' : category,
        }
    return render(request, 'store/home.html', context)
