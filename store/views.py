from django.shortcuts import render, get_object_or_404
from cart.models import CartItem
from .models import Product
from category.models import Category
from cart.views import _cart_id
from django.core.paginator import Paginator
from django.db.models import Q, Min, Max
from django.db.models import Sum, Window


def store(request, category_slug=None):
    categories = None
    products = None

    price = request.GET.get('price', "")

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category= categories, is_available=True).order_by('product_name')
        total_count = Product.objects.all().filter(is_available=True).order_by('product_name').count()


        # sort by 
        sort_by = request.GET.get("sort") 
        if sort_by == "l2h":  
            products = Product.objects.all().filter(is_available =True).order_by('price')
        elif sort_by == "h2l":
            products = Product.objects.all().filter(is_available =True).order_by('-price')
        elif sort_by =='date':
            products = Product.objects.all().filter(is_available =True).order_by('-modified_date')
        
        # order by price
        order_by = request.GET.get("price") 
        if order_by == "1000":  
            products = Product.objects.all().filter(price__lte=1000)
        elif order_by == "10000":
            products = Product.objects.all().filter(price__lte=10000)
        elif order_by =='50000':
            products = Product.objects.all().filter(price__lte=50000)
        elif order_by =='100000':
            products = Product.objects.all().filter(price__lte=100000)

        p = Paginator(products, 4)
        page = request.GET.get('page')
        page_products = p.get_page(page)
        product_count = products.count()         

    else:
        products = Product.objects.all().filter(is_available=True).order_by('product_name')
        total_count = Product.objects.all().filter(is_available=True).order_by('product_name').count()

        # sort by 
        sort_by = request.GET.get("sort") 
        if sort_by == "l2h":  
            products = Product.objects.all().filter(is_available =True).order_by('price')
        elif sort_by == "h2l":
            products = Product.objects.all().filter(is_available =True).order_by('-price')
        elif sort_by =='date':
            products = Product.objects.all().filter(is_available =True).order_by('-modified_date')
        
        # order by price
        order_by = request.GET.get("price") 
        if order_by == "500": 
            products = Product.objects.all().filter(price__lte=500)
        elif order_by == "1000":
            products = Product.objects.all().filter(price__lte=1000)
        elif order_by =='5000':
            products = Product.objects.all().filter(price__lte=5000)
        elif order_by =='10000':
            products = Product.objects.all().filter(price__lte=10000)

        p = Paginator(products, 4)
        page = request.GET.get('page')
        page_products = p.get_page(page)
        product_count = products.count()    

        

    context = { 
        'products' : page_products,
        'product_count' : product_count,
        'total_count' : total_count,

        }
    return render(request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart        = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
        # cart__cart_id means get cart_id from cart
    except Exception as e:
        raise e
    

    context = {
        'single_product' : single_product,
        'in_cart'        : in_cart,
    }
    return render(request, 'store/product_detail.html', context)

def search(request):
    products = None
    product_count    = None
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            # this checks that if the description or product_name contains the keyword or not
            # to check in two columns use Q 
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains= keyword) | Q(product_name__icontains= keyword))
            product_count = products.count()

    context = {
        'products' : products, 
        'product_count' : product_count,
    }
    return render(request, 'store/store.html', context)
