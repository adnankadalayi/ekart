from django.shortcuts import render,redirect
from accounts.models import Accounts
from banner.models import Banner
from orders.models import Order, OrderProduct
from store.models import Product
from category.models import Category
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from .forms import BannerForm, ProductForm, CouponForm
from category.models import Category
from .forms import CategoryForm, CategoryOfferForm, ProductOfferForm
from django.db.models import Q
from django.db.models.functions import Extract, ExtractMonth, TruncMonth, ExtractDay
from django.db.models import Count
from django.core.paginator import Paginator
import calendar
from store.models import ProductOffer, CategoryOffer
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from cart.models import Coupon


def dashboard(request):
    total = 0
    users = Accounts.objects.all().count()
    users_date  = Accounts.objects.annotate(day=ExtractDay('date_joined')).values('day').annotate(total=Count('id'))
    orders      = OrderProduct.objects.annotate(day=ExtractDay('created_at')).values('day').annotate(total=Count('id'))
    order_count = OrderProduct.objects.all().count()
    products    = Product.objects.all().count()
    product_details = Product.objects.annotate(day=ExtractDay('created_date')).values('day').annotate(total=Count('id'))
    ordered_product = OrderProduct.objects.all()

    for i in ordered_product:
        total = 0 + i.product.price

    orders_count = []
    orders_date = []

    for i in orders:
        orders_date.append(i['day'])
        orders_count.append(i['total'])

    users_count = []
    user_date = []

    for i in users_date:
        user_date.append(i['day'])
        users_count.append(i['total'])
    
    product_count = []
    product_date = []

    for i in product_details:
        product_date.append(i['day'])
        product_count.append(i['total'])
   
    context = {
        'orders_count' : orders_count,
        'orders_date' : orders_date,
        'users' : users,
        'order_count' : order_count,
        'products' : products,
        'users_count' : users_count,
        'user_date' : user_date,
        'product_count' : product_count,
        'product_date' : product_date,
        
    }
    return render(request, 'admin/admin_dashboard.html', context)

def user(request):
    user_details = Accounts.objects.all().order_by('date_joined')
    p = Paginator(user_details, 5)
    page = request.GET.get('page')
    page_details = p.get_page(page)
    return render(request, 'admin/admin_user.html', {'user_details': page_details})

def product(request):
    products = Product.objects.all().order_by('created_date')
    p = Paginator(products, 5)
    page = request.GET.get('page')
    page_details = p.get_page(page)
    return render(request, 'admin/admin_product.html',{'products': page_details})
    
def category(request):
    categories = Category.objects.all().order_by('category_name')
    p = Paginator(categories, 1)
    page = request.GET.get('page')
    page_details = p.get_page(page)
    return render(request, 'admin/admin_category.html',{'categories': page_details})

def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
    
        user = auth.authenticate(username= username, password= password)
        
        if user is not None:
            if user.is_admin == True:
                auth.login(request, user)
                return redirect('order')
            else:   
                messages.info(request,'Invalid Credentials')
                return redirect('admin_login')

        else:   
            messages.info(request,'Invalid Credentials')
            return redirect('admin_login')
    else:
        return render(request, 'admin/admin_login.html')


def admin_logout(request):
    auth.logout(request)
    return redirect('admin_login')


def activate_user(request, id):
    user = Accounts.objects.get(id=id)
    user.is_active = True
    user.save()
    return redirect('user')

def deactivate_user(request, id):
    user = Accounts.objects.get(id=id)
    user.is_active = False
    user.save()
    return redirect('user')


def edit_product(request,id):
    initial_value =Product.objects.get(id=id)
    form = ProductForm(instance=initial_value)

    if request.method == 'POST':
       form = ProductForm(request.POST, request.FILES,  instance = initial_value)
       if form.is_valid():
            form.save()
            messages.success(request, 'Product Edited Successfully')
            return redirect('product')
    
    context = {
        'form' : form,
        
    }

    return render(request, 'admin/admin_edit_product.html', context)

def add_product(request):
    form = ProductForm()
                             
    if request.method == 'POST':
       form = ProductForm(request.POST, request.FILES, )
       if form.is_valid():  
            form.save()
            messages.success(request, 'Product Added Successfully')
            return redirect('product')
     
    context = {
        'form' : form
    }
    

    return render(request, 'admin/admin_add_product.html', context) 


def delete_product(request, id):
    product_details = Product.objects.get(id=id)
    product_details.delete()
    return redirect('product')


def edit_category(request,id):
    initial_value =Category.objects.get(id=id)
    form = CategoryForm(instance=initial_value)

    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance = initial_value)
        if form.is_valid():
            if form.save():
                messages.success(request, 'Category Edited Successfully')
                return redirect('category')
    
    context = {
        'form' : form
    }
    return render(request, 'admin/admin_edit_category.html', context)


def delete_category(request, id):
    product_details = Category.objects.get(id=id)
    product_details.delete()
    return redirect('category')



def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():  
            if form.save():
                messages.success(request, 'Category Added Successfully')
                return redirect('category')
    
    context = {
        'form' : form
    }
    return render(request, 'admin/admin_add_category.html', context)  


def order(request):
    orders = OrderProduct.objects.filter()
    context = {
        'orders':orders
    }
    return render(request, 'admin/admin_order.html', context)


def cancel_order_admin(request, order_number):
    order = Order.objects.get( order_number= order_number)
    order.status = 'Cancelled'
    order.save()
    
    return redirect('order')
    
def return_order_admin(request, order_number):
    order = Order.objects.get( order_number= order_number)
    order.status = 'Returned'
    order.save()
    
    return redirect('order')


def deliver_order(request, order_number):
    order = Order.objects.get( order_number= order_number)
    order.status = 'Delivered'
    order.save()
    
    return redirect('order')

def ship_order(request, order_number):
    order = Order.objects.get( order_number= order_number)
    order.status = 'Shipped'
    order.save()
    
    return redirect('order')

def order_order(request, order_number):
    order = Order.objects.get( order_number= order_number)
    order.status = 'Ordered'
    order.save()
    
    return redirect('order')
    
def banner(request):
    banners = Banner.objects.all().order_by('id')
    p = Paginator(banners, 5)
    page = request.GET.get('page')
    page_details = p.get_page(page)
    context = {
        'banners':banners,
        'page_details' : page_details,
    }
    return render(request, 'admin/admin_banner.html', context)

def edit_banner(request,id):
    initial_value =Banner.objects.get(id=id)
    form = BannerForm(instance=initial_value)

    if request.method == 'POST':
        form = BannerForm(request.POST, request.FILES, instance = initial_value)
        if form.is_valid():
            if form.save():
                messages.success(request, 'Banner Edited Successfully')
                return redirect('banner')
    
    context = {
        'form' : form
    }
    return render(request, 'admin/admin_edit_banner.html', context)


def add_banner(request):
    form = BannerForm()

    if request.method == 'POST':
        form = BannerForm(request.POST, request.FILES)
        if form.is_valid():  
            if form.save():
                messages.success(request, 'Banner Added Successfully')
                return redirect('banner')
    
    context = {
        'form' : form
    }
    return render(request, 'admin/admin_add_banner.html', context)  

def delete_banner(request, id):
    banners = Banner.objects.get(id=id)
    banners.delete()
    return redirect('banner')

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            # this checks that if the description or product_name contains the keyword or not
            # to check in two columns use Q 
            products        = Product.objects.order_by('-created_date').filter(Q(description__icontains= keyword) | Q(product_name__icontains= keyword))
            banners         = Banner.objects.order_by('-created_date').filter(Q(subtitle__icontains= keyword) | Q(title__icontains= keyword))
            categories      = Category.objects.order_by('-created_date').filter(Q(category_name__icontains= keyword))
            users           = Accounts.objects.order_by('-created_date').filter(Q(first_name__icontains= keyword) | Q(last_name__icontains= keyword))
            orders          = OrderProduct.objects.order_by('-created_date').filter(Q(order__icontains= keyword) | Q(user__icontains= keyword) | Q(product__icontains= keyword))

    context = {
        'products' : products, 
        'banners' : banners, 
        'categories' : categories, 
        'users' : users, 
        'orders' : orders, 

    }
    return redirect(request, 'admin/admin_product.html', context)

def product_offers(request):
    product_offer = ProductOffer.objects.all().order_by('id')
    p = Paginator(product_offer, 1)
    page = request.GET.get('page')
    page_details = p.get_page(page)

    context = {
        'product_offer' : product_offer, 
        'page_details' : page_details, 
    }
    return render(request, 'admin/admin_product_offers.html', context)

def category_offers(request):
    category_offer = CategoryOffer.objects.all().order_by('id')
    p = Paginator(category_offer, 1)
    page = request.GET.get('page')
    page_details = p.get_page(page)
    

    context = {
        'category_offer' : category_offer, 
        'page_details' : page_details, 
    }
    return render(request, 'admin/admin_category_offers.html', context)

def edit_category_offers(request, id):
    initial_value =CategoryOffer.objects.get(id=id)
    form = CategoryOfferForm(instance=initial_value)

    if request.method == 'POST':
        form = CategoryOfferForm(request.POST, instance = initial_value)
        if form.is_valid():
            if form.save():
                messages.success(request, 'CategoryOffer Edited Successfully')
                return redirect('category_offers')
    
    context = {
        'form' : form
    }
    return render(request, 'admin/admin_edit_category_offers.html', context)

def add_category_offers(request):
    form = CategoryOfferForm()

    if request.method == 'POST':
        form = CategoryOfferForm(request.POST)
        if form.is_valid():  
            if form.save():
                messages.success(request, 'CategoryOffer Added Successfully')
                return redirect('category_offers')
    
    context = {
        'form' : form
    }
    return render(request, 'admin/admin_add_category_offers.html', context)

def edit_product_offers(request, id):
    initial_value =ProductOffer.objects.get(id=id)
    form = ProductOfferForm(instance=initial_value)

    if request.method == 'POST':
        form = ProductOfferForm(request.POST, instance = initial_value)
        if form.is_valid():
            if form.save():
                messages.success(request, 'ProductOffer Edited Successfully')
                return redirect('product_offers')
    
    context = {
        'form' : form
    }
    return render(request, 'admin/admin_edit_product_offers.html', context)

def add_product_offers(request):
    form = ProductOfferForm()

    if request.method == 'POST':
        form = ProductOfferForm(request.POST)
        if form.is_valid():  
            if form.save():
                messages.success(request, 'ProductOffer Added Successfully')
                return redirect('product_offers')
    
    context = {
        'form' : form
    }
    return render(request, 'admin/admin_add_product_offers.html', context)


def delete_category_offers(request, id):
    category_offers = CategoryOffer.objects.get(id=id)
    category_offers.delete()
    return redirect('category_offers')

def delete_product_offers(request, id):
    product_offers = ProductOffer.objects.get(id=id)
    product_offers.delete()
    return redirect('product_offers')

def report_pdf(request):
    # create  bytestream buffer
    buf = io.BytesIO()
    # create a canvas
    cnvs = canvas.Canvas(buf, pagesize=letter, bottomup= 0)
    # create a text object
    textobj = cnvs.beginText()
    textobj.setTextOrigin(inch, inch)
    textobj.setFont("Helvetica", 14)
    
    orders = OrderProduct.objects.all()
    lines = []

    for order in orders:
        lines.append(str(order.user)) 
        lines.append(str(order.payment)) 
        lines.append(str(order.order)) 
        lines.append(str(order.product)) 
        lines.append(str(order.product_price)) 
        lines.append('   ') 
        

    # loop 
    for line in lines:
        textobj.textLine(line)
        

    # finish
    cnvs.drawText(textobj)
    cnvs.showPage()
    cnvs.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='weekly sales report.pdf')

def report(request):
    return render(request, 'admin/admin_report.html')
    
def coupon(request):
    coupon = Coupon.objects.all()
    context = {
        'coupon' : coupon,
    }
    return render(request, 'admin/admin_coupon.html', context )

def add_coupon(request):
    form = CouponForm()
    if request.method == 'POST':
        form = CouponForm(request.POST)
        if form.is_valid():
            if form.save():
                messages.success(request, 'Coupon added successfully')
                return redirect('coupon')

    context = {
        'form': form,
    }
    return render(request, 'admin/admin_add_coupon.html', context)

def edit_coupon(request, id):
    initial_value = Coupon.objects.get(id=id)
    form = CouponForm(instance=initial_value)

    if request.method == 'POST':
        form = CouponForm(request.POST, instance=initial_value)
        if form.is_valid():
            if form.save():
                messages.success(request, 'Coupon Edited Successfully')
                return redirect('coupon')
    context = {
        'form' :form,
    }
    return render(request, 'admin/admin_edit_coupon.html',context)

def delete_coupon(request, id):
    coupon = Coupon.objects.get(id=id)
    coupon.delete()
    return redirect('coupon')
