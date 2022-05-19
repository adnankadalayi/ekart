
from django.urls import path
from . import views

urlpatterns =[
    path('register',views.register, name='register'),
    path('login',views.loginPage, name='loginPage'),
    path('logout',views.logoutPage, name='logoutPage'),
    path('verify',views.verify, name='verify'),
    path('verify_otp',views.verify_otp, name='verify_otp'),
    path('user_orders',views.user_orders, name='user_orders'),
    path('profile',views.profile, name='profile'),
    path('address',views.address, name='address'),
    path('referrals',views.referrals, name='referrals'),
    path('edit_profile',views.edit_profile, name='edit_profile'),
    path('change_password',views.change_password, name='change_password'),
    path('add_address',views.add_address, name='add_address'),
    path('edit_address/<slug:id>',views.edit_address, name='edit_address'),
    path('delete_address/<slug:id>',views.delete_address, name='delete_address'),
    path('activate_address',views.activate_address, name='activate_address'),
    path('cancel_order/<int:order_number>',views.cancel_order,name='cancel_order'),

]