from django.urls import path
from . import views 
from django.views.i18n import JavaScriptCatalog


urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
    path('user', views.user, name='user'),
    path('product', views.product, name='product'),
    path('category', views.category, name='category'),
    path('', views.admin_login, name='admin_login'),
    path('logout', views.admin_logout, name='admin_logout'),
    path('product/delete/<int:id>', views.delete_product, name='delete_product'),
    path('product/edit/<int:id>', views.edit_product, name='edit_product'),
    path('product/add/', views.add_product, name='add_product'),
    path('user/deactivate/<int:id>', views.deactivate_user, name='deactivate_user'),
    path('user/activate/<int:id>', views.activate_user, name='activate_user'),
    path('category/edit/<int:id>', views.edit_category, name='edit_category'),
    path('category/delete/<int:id>', views.delete_category, name='delete_category'),
    path('category/add/', views.add_category, name='add_category'),
    path('order', views.order, name='order'),
    path('cancel_order_admin/<int:order_number>',views.cancel_order_admin,name='cancel_order_admin'),
    path('return_order_admin/<int:order_number>',views.return_order_admin,name='return_order_admin'),
    path('order_order/<int:order_number>',views.order_order,name='order_order'),
    path('ship_order/<int:order_number>',views.ship_order,name='ship_order'),
    path('deliver_order/<int:order_number>',views.deliver_order,name='deliver_order'),
    path('banner', views.banner, name='banner'),
    path('banner/add/', views.add_banner, name='add_banner'),
    path('banner/edit/<int:id>', views.edit_banner, name='edit_banner'),
    path('banner/delete/<int:id>', views.delete_banner, name='delete_banner'),
    path('search/', views.search, name='admin_search'),
    path('category_offers', views.category_offers, name='category_offers'),
    path('category_offers/add/', views.add_category_offers, name='add_category_offers'),
    path('category_offers/edit/<int:id>', views.edit_category_offers, name='edit_category_offers'),
    path('product_offers', views.product_offers, name='product_offers'),
    path('product_offers/add/', views.add_product_offers, name='add_product_offers'),
    path('product_offers/edit/<int:id>', views.edit_product_offers, name='edit_product_offers'),
    path('category_offers/delete/<int:id>', views.delete_category_offers, name='delete_category_offers'),
    path('product_offers/delete/<int:id>', views.delete_product_offers, name='delete_product_offers'),
    path('report_pdf', views.report_pdf, name='report_pdf'),
    path('report', views.report, name='report'),
    path('coupon', views.coupon, name='coupon'),
    path('coupon/add', views.add_coupon, name='add_coupon'),
    path('coupon/edit/<int:id>', views.edit_coupon, name='edit_coupon'),
    path('coupon/delete/<int:id>', views.delete_coupon, name='delete_coupon'),


]