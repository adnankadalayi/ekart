import random 
from django.shortcuts import render, redirect
from accounts.models import Accounts, Address
from cart .models import Cart, CartItem
from orders.forms import OrderForm, UserAddressForm
from orders.models import Order, OrderProduct, Payment
import datetime
from django.contrib import messages
from store.models import Product
from django.http import HttpResponse, JsonResponse
import json
import razorpay
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa

def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("cp1252", 'ignore')), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None


#Automaticly downloads to PDF file
class DownloadPDF(View):
	def get(self, request, *args, **kwargs):
		
		pdf = render_to_pdf('store/invoice_content.html', data)

		response = HttpResponse(pdf, content_type='application/pdf')
		filename = "Invoice_%s.pdf" %("12341231")
		content = "attachment; filename='%s'" %(filename)
		response['Content-Disposition'] = content
		return response

def paypal_payments(request):
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, is_ordered= False, order_number=body['orderID'])
    # saving the order in payment model
    payment = Payment(
        user = request.user,
        payment_id= body['transID'], 
        payment_method= body['payment_method'],
        amount_paid=  body['total'], 
        status= body['status'],
    )
    payment.save()

    order.payment = payment
    order.is_ordered = True
    order.save()
    # move the cart items to orderproduct table
    cart_items = CartItem.objects.filter(user=request.user)

    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True 
        orderproduct.save() 

        # reduce the quantity from the stock
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()

    # clear cart
    CartItem.objects.filter(user=request.user).delete()
    # send transaction id and order number back to sendData via jsonresponse
    data = {
        'order_number': order.order_number,
        'transID' : payment.payment_id, 
    }
    return JsonResponse(data)

def paypal_success(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')
    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_product = OrderProduct.objects.filter(order_id= order.id)
        payment = Payment.objects.get(payment_id=transID)

        subtotal = 0
        for i in ordered_product:
            subtotal += i.product_price * i.quantity
        context = {
            'order' : order,
            'ordered_product' : ordered_product, 
            'order_number' : order.order_number,
            'payment_id' : payment.payment_id,
            'payment' : payment,
            'subtotal' : subtotal,
            'tax' : order.tax, 
            'total' : order.order_total,
        }
        return render(request,'store/invoice.html', context)
    except (Order.DoesNotExist, Payment.DoesNotExist):
        return redirect('home')

def order_status(request):

    order = Order.objects.get(user = request.user, is_ordered  =False )
    
    #  store transaction details in payment model
    payment = Payment(
        user = request.user,
        payment_id = random.randrange(100000, 999999),
        payment_method = 'Cash on Delivery',
        amount_paid = order.order_total,
        status = 'Order Placed',

    )
    payment.save()

    order.payment = payment
    order.is_ordered = True
    order.save()

    total= 0
    quantity = 0
    tax = 0
    grand_total = 0
    shipping = 50
    cart_items = CartItem.objects.filter( user= request.user, is_active=True).order_by('product')
   
    for cart_item in cart_items:
        total +=(cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax= (3 * total)//100
    grand_total = total + tax + shipping

    context ={
        'order':order,
        'cart_items' : cart_items,
        'total':total,
        'tax':tax,
        'shipping':shipping,
        'grand_total':grand_total,
        'quantity':quantity,
        'payment':payment,
    }
    return render(request,'store/invoice.html', context)

def place_order(request, total=0, quantity=0):
    current_user = request.user

    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user = current_user)
    else:
        # requesting cookies from device that already set on base.html named device
        device = request.COOKIES['device']
        cart_items = CartItem.objects.filter(device = device)
    cart_count = cart_items.count()
    #  if cart is less than or equal to 0 then the user should redirect to store
    if cart_count <= 0:
        return redirect('store')
    tax = 0
    grand_total = 0
    shipping = 50

    data = Order()
    
    try:
        address_id = request.POST['ship_address']
        
    except:
        messages.error(request,'Select a valid address')
        return redirect('checkout')


    cart_items = CartItem.objects.filter(user=request.user)

    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity

    tax= (3 * total)//100
    shipping = 50
    grand_total = total + tax + shipping

    if request.method == 'POST':
        address_id = request.POST['ship_address']
        address = Address.objects.filter(id = address_id, user = request.user.id)
        order_note = request.POST['order_note']
        user = request.user
        for i in address:
            first_name = i.first_name
            last_name = i.last_name
            phone_no = i.phone_no
            email = i.email
            address_line_1 = i.address_line_1
            address_line_2 = i.address_line_2
            country = i.country
            state = i.state
            city = i.city
            pin  = i.pin
        current_user = request.user
        order_number =  request.session['order_number'] 

        cart_items = CartItem.objects.filter(user=request.user)

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity

        tax= (3 * total)//100
        shipping = 50
        grand_total = total + tax + shipping
        
        # Store all the billing information inside Order table
        order = Order.objects.get(user=current_user,is_ordered = False, order_number = order_number)
        
        order.first_name         = first_name
        order.last_name          = last_name
        order.phone_no           = phone_no
        order.email              = email
        order.address_line_1     = address_line_1
        order.address_line_2     = address_line_2
        order.country            = country
        order.state              = state
        order.city               = city
        order.order_note         = order_note
        order.pin                = pin
        order.save()        
            
        track_number        = 'order'+str(random.randint(1111111,9999999))
        while Order.objects.filter(tracking_no=track_number) is None:
            track_number        = 'order'+str(random.randint(1111111,9999999))
        order.tracking_no    = track_number
        order.save()

        # create a object for this 
        order = Order.objects.get(user= current_user, is_ordered=False, order_number=order_number)
        order_items = CartItem.objects.filter(user=current_user)
        
        for item in order_items :
            OrderProduct.objects.create(
                order= order,
                user = current_user,
                product= item.product,
                product_price= item.product.price,  
                quantity= item.quantity,
            )
            # to decrease the product for available stock
            order_product = Product.objects.filter(id= item.product_id).first()
            order_product.stock = order_product.stock - item.quantity
            order_product.save()

            #  clear the cart after order placed
            CartItem.objects.filter(user= request.user).delete()
            messages.success(request, 'Your order has been placed Successfully.')  
        
        order.is_ordered = True
        order.save()
    
        context = {
            'order': order,
            'cart_items' : cart_items,
            'total':total,
            'tax':tax,
            'grand_total': grand_total,
            'shipping' : shipping,
        }
        return render(request,'store/order_status.html',context)
    else:
        return redirect('checkout')


def order_details(request, tr_no):
    order = Order.objects.filter(tracking_no= tr_no).filter(user= request.user).first()
    order_items = OrderProduct.objects.filter(order= order)
    context = {
        'order':order,
        'order_items':order_items,
    }
    return render(request, 'store/order_details.html', context)



def return_order(request, order_number):
    order = Order.objects.get( order_number= order_number)
    order.status = 'Returned'
    order.save()
    
    return redirect('user_orders')
    