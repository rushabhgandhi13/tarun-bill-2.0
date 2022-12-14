from django.urls import path
from django.urls import include

from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),

    path('invoices/new', views.invoice_create, name='invoice_create'),
    path('invoices/delete', views.invoice_delete, name='invoice_delete'),

    path('login', views.login_view, name='login_view'),
    path('accounts/', include('django.contrib.auth.urls')),

    path('invoices', views.invoices, name='invoices'),
    path('invoice/<int:invoice_id>', views.invoice_viewer, name='invoice_viewer'),
    path('challan/<int:invoice_id>', views.challan_viewer, name='challan_viewer'),
    path('invoice_scanned/<int:invoice_id>', views.invoice_scanned, name='invoice_scanned'),
    # path('invoice-download/<id>', views.generate_PDF, name='invoice-download'),
    # path('challan-download/<id>', views.generate_challan, name='challan-download'),
    # path('invoice-scanned/<id>', views.generate_invoice, name='invoice-scanned'),

    path('customers', views.customers, name='customers'),
    path('customers/add', views.customer_add, name='customer_add'),
    path('customers/edit/<int:customer_id>', views.customer_edit, name='customer_edit'),
    path('customers/delete', views.customer_delete, name='customer_delete'),
    path('customersjson', views.customersjson, name='customersjson'),

    path('products', views.products, name='products'),
    path('products/add', views.product_add, name='product_add'),
    path('products/edit/<int:product_id>', views.product_edit, name='product_edit'),
    path('products/delete', views.product_delete, name='product_delete'),
    path('productsjson', views.productsjson, name='productsjson'),





]