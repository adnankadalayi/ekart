from django.urls import path
from . import views 


urlpatterns = [
  path('', views.cart, name='cart'),
  path('add_cart/<int:product_id>/', views.add_cart, name='add_cart'),
  path('order_now/<int:product_id>/', views.order_now, name='order_now'),
  path('remove_cart/<int:product_id>/', views.remove_cart, name='remove_cart'),
  path('remove_cart_item/<int:product_id>/', views.remove_cart_item, name='remove_cart_item'),
  path('checkout', views.checkout, name='checkout'),
  path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
  path('coupon_apply/', views.coupon_apply, name='coupon_apply'),
  path('updatecart', views.updateCart, name='update_cart'),


]