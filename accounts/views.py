from multiprocessing import context
from django.shortcuts import redirect, render
from admin_panel.views import user
from cart.models import Cart, CartItem
from orders.forms import OrderForm, UserAddressForm
from orders.models import Order, OrderProduct
from .forms import RegistraionForm
from . models import Accounts, Address, Referral
from django.contrib import messages , auth
from django.contrib.auth.decorators import login_required
import http.client
conn = http.client.HTTPSConnection("2factor.in")
import random
from cart.views import _cart_id
import requests
from . forms import UserProfileUpdateForm, UserAddressUpdateForm, UserPasswordForm
from django.contrib.auth import update_session_auth_hash



#register function
def register(request):
    profile_id = request.session.get('ref_profile')
    if request.method == 'POST':


        form = RegistraionForm(request.POST)
        if form.is_valid():
            if profile_id is not None:
                recommended_by_profile = Referral.objects.get(id=profile_id)

                first_name  = form.cleaned_data['first_name']
                last_name   = form.cleaned_data['last_name']
                phone_no    = form.cleaned_data['phone_no']
                username =  form.cleaned_data['username']
                email       = form.cleaned_data['email']
                
                password = form.cleaned_data['password']
            
                user = Accounts.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
                user.phone_no = phone_no

                # saving form for referral system///actually form here iam user 
                instance = user.save()
                registered_user = Accounts.objects.get(id = user.id)
                registered_profile = Referral.objects.get(user=registered_user) 
                registered_profile.recommended_by = recommended_by_profile.user
                registered_profile.save()
            else:

                first_name  = form.cleaned_data['first_name']
                last_name   = form.cleaned_data['last_name']
                phone_no    = form.cleaned_data['phone_no']
                username =  form.cleaned_data['username']
                email       = form.cleaned_data['email']
                
                password = form.cleaned_data['password']
            
                user = Accounts.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
                user.phone_no = phone_no
                user.save()

            # otp account verification
            request.session["mobile"] = phone_no
            user = Accounts.objects.filter(phone_no=phone_no)

            for m in user:
                if m.phone_no == phone_no:
                    user_mobile = phone_no
                    user_mobile
                    
                    generated_otp = random.randrange(1000,9999)
                    
                    request.session['backend_otp'] = generated_otp

                    conn.request("GET", "/API/V1/f1ba1f56-bc7a-11ec-9c12-0200cd936042/VOICE/"+str(user_mobile)+"/"+str(generated_otp))

                    request.session['phone_no'] = phone_no   
                    return redirect('verify_otp')

    else:
       
        form = RegistraionForm()

    context = {
        'form' : form,
    }
    return render(request, 'store/register.html', context)

def verify_otp(request):

    try:
        if request.method == 'POST':
            generated_otp = request.session.get('backend_otp')
            user_otp = request.POST.get('otp')

            if int(user_otp) == int(generated_otp):
                # messages.success(request, "OTP verified successfully.")
                phone_no = request.session.get('phone_no')
                user = Accounts.objects.get(phone_no=phone_no)
                user.is_active = True
                user.save()
                auth.login(request, user)
                
                return redirect('home')
            else:
                messages.error(request, 'Invalid OTP')
                return redirect('verify_otp')

        else:
            return render(request, 'store/verify_otp.html')
    except:
        messages.error(request, "Enter a valid OTP")
        return render(request, 'store/verify_otp.html')

#login function   
def loginPage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
    
        user = auth.authenticate( username= username, password= password)
        
        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)
                    
                    for item in cart_item:
                        item.user = user
                        item.save()

            except:
                pass
            auth.login(request, user)
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                #  here we get the query next=/cart/checkout
                # we split this to get the url for checkout
                
                cut_url = dict(x.split('=') for x in query.split('&'))
                if 'next' in cut_url:
                    next_page = cut_url['next']
                return redirect(next_page)

            except:
                return redirect('home')

        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('loginPage')
    else:
        return render(request, 'store/login.html')

#logout function
@login_required(login_url='loginPage')
def logoutPage(request):
    auth.logout(request)
    return redirect('loginPage')


def verify(request, **generated_otp):
    if request.method == 'POST':
        phone_no = request.POST['phone_no']

        user = Accounts.objects.filter(phone_no=phone_no)
        for i in user:
            if i.phone_no == phone_no:
                user_mobile = phone_no
            
                generated_otp = random.randrange(1000,9999)
                
                request.session['backend_otp'] = generated_otp
                conn.request("GET", "/API/V1/f1ba1f56-bc7a-11ec-9c12-0200cd936042/SMS/"+str(user_mobile)+"/"+str(generated_otp))

                request.session['phone_no'] = phone_no                    

 
                return redirect('verify_otp')
        else:
            messages.error(request, 'Enter correct Phone Number')
            return redirect('verify')
    return render(request, 'store/verify.html')


@login_required(login_url='loginPage')
def user_orders(request):
    orders = OrderProduct.objects.filter(user = request.user).order_by('-created_at')
    context = {
        'orders':orders
    }
    return render(request, 'store/user_orders.html', context)


@login_required(login_url='loginPage')
def profile(request):
    user_details = Accounts.objects.get(id= request.user.id)
    refers = Referral.objects.get(user= request.user)
    my_recommends = refers.get_recommended_profiles()

    your_code = refers.get_your_refer_code()

    context ={
        'user_details' : user_details,
        'my_recommends' : my_recommends,
        'your_code' : your_code,
    }
    return render(request, 'store/profile.html', context)
@login_required(login_url='loginPage')
def referrals(request):
    refers = Referral.objects.get(user= request.user)
    my_recommends = refers.get_recommended_profiles()

    your_code = refers.get_your_refer_code()

    context ={
        'my_recommends' : my_recommends,
        'your_code' : your_code,
    }
    return render(request, 'store/refers.html', context)

@login_required(login_url='loginPage')
def address(request):
    address         = Address.objects.filter(user= request.user)

    context ={
        'address' : address,
    }
    return render(request, 'store/addresses.html', context)

@login_required(login_url='loginPage')
def edit_profile(request):
    if request.method == 'POST':
        
        form = UserProfileUpdateForm(request.POST, instance= request.user)

        if form.is_valid():
            form.save()

            messages.success(request, 'Profile Edited Successfully')
            return redirect('profile')
    else:
        form = UserProfileUpdateForm(instance = request.user)
    context = {
        'form' : form , 
    }
    
    return render(request, 'store/edit_profile.html', context)


@login_required(login_url='loginPage')
def change_password(request):
    if request.method == 'POST':
        
        # here we need to assign request user to a user not instance 
        form = UserPasswordForm(data=request.POST, user= request.user)

        if form.is_valid():
            form.save()
            # this is used for user to stay in the page after changing password 
            # without this user will redirect to login page
            update_session_auth_hash(request, form.user)

            messages.success(request, 'Password Edited Successfully')
            return redirect('profile')
    else:
        form = UserPasswordForm(user = request.user)
    context = {
        'form' : form , 
    }
    
    return render(request, 'store/change_password.html', context)
    
@login_required(login_url='loginPage')
def add_address(request):
    if request.method == 'POST':

        form = UserAddressForm(data = request.POST)
        
        if form.is_valid():
            #  we need to add user here to connect this form to the exact user
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            return redirect('address')
        else:
            return redirect('add_address')

    else:
        form = UserAddressForm()
    context = {
        'form' : form,
    }
    return render(request, 'store/add_address.html', context)

@login_required(login_url='loginPage')
def edit_address(request, id):
     
    if request.method == 'POST':
        
        address = Address.objects.get(id= id, user = request.user)
        form = UserAddressForm(data = request.POST, instance= address)

        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()

            messages.success(request, 'Address Edited Successfully')
            return redirect('address')
    else:
        address = Address.objects.get(id= id, user = request.user)
        form = UserAddressForm(instance= address)
    context = {
        'form' : form , 
        'address' : address
    }
    
    return render(request, 'store/edit_address.html', context)

@login_required(login_url='loginPage')
def delete_address(request, id):
    address = Address.objects.get(id= id , user = request.user).delete()  
    messages.success(request, 'Address Deleted Successfully')
    return redirect('address')        

def activate_address(request):
    user = request.user
    custid = request.GET.get('custid')
    if custid == None:
        messages.error(request, 'Please Choose a Address')
        return redirect('checkout') 
    
    address = Address.objects.get(id=custid)
    order  = Order.objects.filter(user =user)
   
    return redirect('checkout') 
    
def cancel_order(request, order_number):
    order = Order.objects.get( order_number= order_number)
    order.status = 'Cancelled'
    order.save()
    
    return redirect('user_orders')
    