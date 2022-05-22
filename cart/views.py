from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from accounts.models import Address
from cart.models import Cart, CartItem
from orders.models import Order, OrderProduct
from store.models import Product, CategoryOffer, ProductOffer
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Coupon
from .forms import CouponApplyForm
from django.contrib import messages
import razorpay
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from Ekart.settings import RAZOR_KEY_ID, RAZOR_KEY_SECRET
import json
from django.utils import timezone
import datetime
import random
from django.conf import settings



def _cart_id(request):# by putting underscore infront of this make it private function
    cart = request.session.session_key
    if not cart:# if there is no session it will create a new session
        cart = request.session.create()
    return cart



def remove_cart(request, product_id,):
    product = get_object_or_404(Product, id=product_id)#it will give product or 404
    # here actually try except is used but i didn't with except is pass
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user= request.user)
    else:
        cart = Cart.objects.get(cart_id = _cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart)

    if cart_item.quantity > 1:
        cart_item.quantity  -= 1
        cart_item.save()
    else:
        cart_item.delete()
    # except is used here with pass
    return redirect('cart')



def remove_cart_item(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user= request.user)
    else:
        cart = Cart.objects.get(cart_id= _cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart)    
    cart_item.delete()
    return redirect('cart')



def add_cart(request, product_id):
    product = Product.objects.get(id= product_id) # get the product
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request) ) # get the cart using the cart_id present in the  session
    except Cart.DoesNotExist:# if cart is not present then it create a cart
        cart = Cart.objects.create(
            cart_id = _cart_id(request)

        )
        cart.save()

    if request.user.is_authenticated:
        try:
            cart_item = CartItem.objects.get(product= product, user= request.user)
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
            product = product,
            quantity = 0, 
            cart = cart,
            user = request.user,
        )
        cart_item.save()
    else:
        try:
            cart_item = CartItem.objects.get(product= product, cart= cart)
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
            product = product,
            quantity = 0, 
            cart = cart,
        )
        cart_item.save()
    cart_item.quantity += 1
    cart_item.save()
   
 
    return redirect('cart')

def order_now(request, product_id):
    product = Product.objects.get(id= product_id) # get the product
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request) ) # get the cart using the cart_id present in the  session
    except Cart.DoesNotExist:# if cart is not present then it create a cart
        cart = Cart.objects.create(
            cart_id = _cart_id(request)

        )
        cart.save()

    if request.user.is_authenticated:
        try:
            cart_item = CartItem.objects.get(product= product, user= request.user)
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
            product = product,
            quantity = 0, 
            cart = cart,
            user = request.user,
        )
        cart_item.save()
    else:
        try:
            cart_item = CartItem.objects.get(product= product, cart= cart)
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
            product = product,
            quantity = 0, 
            cart = cart,
        )
        cart_item.save()
    cart_item.quantity += 1
    cart_item.save()
   
 
    return redirect('checkout')
    
def offer_check_function(item):
    product = Product.objects.get(product_name=item)
    if ProductOffer.objects.filter(product=product).exists():
        if product.prod_offers.discount:
            sub_total = product.price - product.price*product.prod_offers.discount//100
        else:
            sub_total=product.price
    elif CategoryOffer.objects.filter(category=item.product.category).exists():

        if product.category.cate_offers:
            sub_total = product.price - product.price*item.product.category.cate_offers.discount//100
        else:
            sub_total=product.price
    else:
        sub_total=product.price
    return sub_total
        
    

def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        sub_total = 0
        shipping = 50
        coupon = None
        deduction = None
        new_total = 0
        final_price = 0
        new_tax = 0

        products = Product.objects.all()
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter( user= request.user, is_active=True).order_by('product')
        else:
            cart = Cart.objects.get(cart_id= _cart_id(request))
            cart_items= CartItem.objects.filter(cart= cart, is_active=True).order_by('product')
        for cart_item in cart_items:
            new_price =  offer_check_function(cart_item)
            sub_total += (new_price * cart_item.quantity)

        tax= (3 * sub_total)//100
        grand_total = sub_total + tax + shipping
        

        coupon_form = CouponApplyForm()
        # checking coupon present or not in session
        if request.session:
            coupon_id = request.session.get('coupon_id')
            try:
                coupon = Coupon.objects.get(id=coupon_id)
                final_price = sub_total-coupon.discount
                new_tax= (3 * final_price)//100
                new_total = final_price + new_tax + shipping
            except:
                pass
            
        else:
            grand_total = grand_total

    except ObjectDoesNotExist:
        pass
        try:
            order = Order.objects.get(user= current_user, is_ordered=False)
        except ObjectDoesNotExist:
            message.info(request, 'Order not found')
            return redirect('cart')
    context ={
        'total' : sub_total,
        'quantity' : quantity,
        'cart_items' : cart_items,
        'tax' : tax,
        'grand_total' : grand_total,
        'shipping' : shipping,
        'coupon_form':coupon_form,
        'coupon':coupon,
        'final_price':final_price,
        'new_total': new_total,
        'new_tax': new_tax,
    }
    return render(request, 'store/cart.html', context)



@login_required(login_url='loginPage')
def checkout(request, total=0, quantity=0, cart_items=None):
    tax = 0
    grand_total = 0
    sub_total = 0
    shipping = 50 
    coupon = None
    final_price = None
    new_total = None
    new_tax = None
    guest_email_id = request.session.get('guest_email_id') 

    try:
        
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True) 
        elif guest_email_id is not None:
            guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, user=guest_email_obj.id) 
        else:

            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        current_user = request.user
        cart_items = CartItem.objects.filter(user=current_user)
        cart_count = cart_items.count()
        if cart_count <=0:
            return redirect('store')

        for cart_item in cart_items:
            new_price =  offer_check_function(cart_item)
            sub_total += (new_price * cart_item.quantity)
        tax= (3 * sub_total)//100
        shipping = 50
        grand_total = sub_total + tax + shipping
        if request.session:
            coupon_id = request.session.get('coupon_id')
            try:
                coupon = Coupon.objects.get(id=coupon_id)
                final_price = sub_total-coupon.discount
                new_tax= (3 * final_price)//100
                new_total = final_price + new_tax + shipping
            except:
                pass
        current_user = request.user
        order = Order()
          #Generate the order number
        order.user               = current_user
        order.tax               = tax
        yr                      = int(datetime.date.today().strftime('%Y'))
        dt                      = int(datetime.date.today().strftime('%d'))
        mt                      = int(datetime.date.today().strftime('%m'))
        d                       = datetime.date(yr,mt,dt)
        current_date            = d.strftime("%Y%m%d")
        order.order_total       = grand_total
        order.save()
        order_number            = current_date + str(random.randint(1111111,9999999))
        order.order_number      = order_number

        
        order.save()
        request.session['order_number'] = order_number
    except ObjectDoesNotExist:
        pass #just ignore
    address = Address.objects.filter(user=request.user)
    razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
    razorpay_order = razorpay_client.order.create(dict(amount=int(order.order_total)*100,
                                                       currency='INR',
                                                       payment_capture='0'))
 
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    
    context ={
        'razor':int(order.order_total)*100,
        'total' : sub_total,
        'quantity' : quantity,
        'cart_items' : cart_items,
        'tax' : tax,
        'grand_total' : grand_total ,
        'shipping' : shipping,
        'address' : address,
        'coupon' : coupon,
        'final_price':final_price,
        'new_total': new_total,
        'new_tax': new_tax,
        'order' : order,
        'razorpay_order_id':razorpay_order_id,

    }

    return render(request, 'store/checkout.html', context)

@csrf_exempt
def paymenthandler(request):
    
    # only accept POST request.
    if request.method == "POST":
        
        payment_id = request.POST.get('razorpay_payment_id', '')
        razorpay_order_id = request.POST.get('razorpay_order_id', '')
        signature = request.POST.get('razorpay_signature', '')
       
        order_number=razorpay_order_id
        # create a object for this 
        order = Order.objects.filter(user= request.user, is_ordered=False, order_number=razorpay_order_id)
        order_items = CartItem.objects.filter(user=request.user)
        
        
        # for item in order_items :
        #     OrderProduct.objects.create(
        #         order=order,
        #         user = request.user,
        #         product= item.product,  
        #         product_price= item.product.price,  
        #         quantity= item.quantity,
        #     )
        #     # to decrease the product for available stock
        #     order_product = Product.objects.filter(id= item.product_id).first()
        #     order_product.stock = order_product.stock - item.quantity
        #     order_product.save()
        #     order.is_ordered = True
        #     order.save()
        #     #  clear the cart after order placed
        CartItem.objects.filter(user= request.user).delete()

    context = {
        'order' : order,
    }
    return render(request,'store/razor_success.html',context)

def coupon_apply(request):
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__iexact=code, valid_from__lte=now, valid_to__gte=now, is_active=True)
            request.session['coupon_id'] = coupon.id
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None
            messages.error(request, 'Entered Coupon is not available')

    return redirect('cart')


def updateCart(request):
    data = json.loads(request.body)
    product_id = data['product_id']
    action = data['action']
    if request.user.is_authenticated:
        customer = request.user
        product = Product.objects.get(product_id= product_id)
        cart, created = Cart.objects.get_or_create(owner=customer, completed=False)
        cartitems, created = Cartitems.objects.get_or_create(product=product, cart=cart)

        if action == 'add':
            cartitems.quantity += 1
        cartitems.save()

        msg = {
            'quantity': cart.cartquantity
        }

    return JsonResponse(msg, safe=False)