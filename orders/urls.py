
from django.urls import path
from . import views

urlpatterns =[
   path('place_order',views.place_order,name='place_order'),
   path('order_status',views.order_status,name='order_status'),
   path('order_details/<str:tr_no>',views.order_details,name='order_details'),
   path('return_order/<int:order_number>',views.return_order,name='return_order'),
   path('paypal_payments/',views.paypal_payments,name='paypal_payments'),
   path('order_success/',views.paypal_success,name='order_success'),
   path('pdf_download/', views.DownloadPDF.as_view(), name="pdf_download"),
]