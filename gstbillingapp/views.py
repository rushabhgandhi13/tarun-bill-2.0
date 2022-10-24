import datetime
import decimal
import json
import num2words

from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.http import JsonResponse
from django.db.models import Max

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import Customer, Financial_year, Payment_terms, Place_of_supply, Transporter_info, Vehicle
from .models import Invoice
from .models import Product


from .utils import invoice_data_validator
from .utils import invoice_data_processor
from .forms import CustomerForm
from .forms import ProductForm

# Create your views here.


# User Management =====================================







def login_view(request):
    if request.user.is_authenticated:
        return redirect("invoice_create")
    context = {}
    auth_form = AuthenticationForm(request)
    if request.method == "POST":
        auth_form = AuthenticationForm(request, data=request.POST)
        if auth_form.is_valid():
            user = auth_form.get_user()
            if user:
                login(request, user)
                return redirect("invoice_create")
        else:
            context["error_message"] = auth_form.get_invalid_login_error()
    context["auth_form"] = auth_form
    return render(request, 'gstbillingapp/login.html', context)


def signup_view(request):
    if request.user.is_authenticated:
        return redirect("invoice_create")
    context = {}
    signup_form = UserCreationForm()
    profile_edit_form = UserProfileForm()
    context["signup_form"] = signup_form
    context["profile_edit_form"] = profile_edit_form

    
    if request.method == "POST":
        signup_form = UserCreationForm(request.POST)
        profile_edit_form = UserProfileForm(request.POST)
        context["signup_form"] = signup_form
        context["profile_edit_form"] = profile_edit_form

        if signup_form.is_valid():
            user = signup_form.save()
        else:
            context["error_message"] = signup_form.errors
            return render(request, 'gstbillingapp/signup.html', context)
        if profile_edit_form.is_valid():
            userprofile = profile_edit_form.save(commit=False)
            userprofile.user = user
            userprofile.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect("invoice_create")



    return render(request, 'gstbillingapp/signup.html', context)



# Invoice, products and customers ===============================================

@login_required
def invoice_create(request):
    # if business info is blank redirect to update it

    context = {}
    context['default_invoice_number'] = Invoice.objects.all().aggregate(Max('invoice_number'))['invoice_number__max']
    if not context['default_invoice_number']:
        context['default_invoice_number'] = 1
    else:
        context['default_invoice_number'] += 1

    context['default_invoice_date'] = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
    context['place_of_supply']= Place_of_supply.objects.all()
    context['transporter']= Transporter_info.objects.all()
    context['vehicles']= Vehicle.objects.all()
    context['financial_year']= Financial_year.objects.all()
    context['payment_terms']= Payment_terms.objects.all()

    if request.method == 'POST':
        print("POST received - Invoice Data")

        invoice_data = request.POST

        validation_error = invoice_data_validator(invoice_data)
        if validation_error:
            context["error_message"] = validation_error
            return render(request, 'gstbillingapp/invoice_create.html', context)

        # valid invoice data
        print("Valid Invoice Data")

        invoice_data_processed = invoice_data_processor(invoice_data)
        # save customer
        customer = None

        try:
            customer = Customer.objects.get(customer_name=invoice_data['customer-name'],
                                            customer_address=invoice_data['customer-address'],
                                            customer_gst=invoice_data['customer-gst'])
        except:
            print("===============> customer not found")
            print(invoice_data['customer-name'])
            print(invoice_data['customer-address'])
            print(invoice_data['customer-gst'])

        if not customer:
            print("CREATING CUSTOMER===============>")
            customer = Customer(
                customer_name=invoice_data['customer-name'],
                customer_address=invoice_data['customer-address'],
                customer_gst=invoice_data['customer-gst'])
            # create customer book
            customer.save()

        # save product
        # update_products_from_invoice(invoice_data_processed, request)


        # save invoice
        invoice_data_processed_json = json.dumps(invoice_data_processed)
        new_invoice = Invoice(
                              invoice_number=int(invoice_data['invoice-number']),
                              invoice_date=datetime.datetime.strptime(invoice_data['invoice-date'], '%Y-%m-%d'),
                              invoice_customer=customer, invoice_json=invoice_data_processed_json)
        new_invoice.save()
        print("INVOICE SAVED")



        return redirect('invoice_viewer', invoice_id=new_invoice.id)

    return render(request, 'gstbillingapp/invoice_create.html', context)


@login_required
def invoices(request):
    context = {}
    context['invoices'] = Invoice.objects.all().order_by('-id')
    return render(request, 'gstbillingapp/invoices.html', context)


@login_required
def invoice_viewer(request, invoice_id):
    def num2words(num):
        num = decimal.Decimal(num)
        decimal_part = num - int(num)
        num = int(num)

        if decimal_part:
            return num2words(num) + " And Paise " + (" ".join(num2words(i) for i in str(decimal_part)[2:]))

        under_20 = ['Zero', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Eleven', 'Twelve', 'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen', 'Seventeen', 'Eighteen', 'Nineteen']
        tens = ['Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty', 'Seventy', 'Eighty', 'Ninety']
        above_100 = {100: 'Hundred', 1000: 'Thousand', 100000: 'Lakhs', 10000000: 'Crores'}

        if num < 20:
            return under_20[num]

        if num < 100:
            return tens[num // 10 - 2] + ('' if num % 10 == 0 else ' ' + under_20[num % 10])

        # find the appropriate pivot - 'Million' in 3,603,550, or 'Thousand' in 603,550
        pivot = max([key for key in above_100.keys() if key <= num])

        return num2words(num // pivot) + ' ' + above_100[pivot] + ('' if num % pivot==0 else ' ' + num2words(num % pivot))

    invoice_obj = get_object_or_404(Invoice, id=invoice_id)

    context = {}
    context['invoice'] = invoice_obj
    context['invoice_data'] = json.loads(invoice_obj.invoice_json)
    print(context['invoice_data'])
    context['currency'] = "₹"
    context["total_cartons"] = int(context['invoice_data']['cartons'])+int(context['invoice_data']['bundles'])
    context['total_in_words'] = num2words(format(float(context['invoice_data']['invoice_total_amt_with_gst']), '.2f'))
    context['user_profile'] = user_profile
    return render(request, 'gstbillingapp/tax_invoice_template.html', context)


@login_required
def invoice_delete(request):
    if request.method == "POST":
        invoice_id = request.POST["invoice_id"]
        invoice_obj = get_object_or_404(Invoice, id=invoice_id)
        invoice_obj.delete()
    return redirect('invoices')


@login_required
def customers(request):
    context = {}
    context['customers'] = Customer.objects.all()
    return render(request, 'gstbillingapp/customers.html', context)


@login_required
def products(request):
    context = {}
    context['products'] = Product.objects.all()
    return render(request, 'gstbillingapp/products.html', context)


@login_required
def customersjson(request):
    customers = list(Customer.objects.all().values())
    return JsonResponse(customers, safe=False)


@login_required
def productsjson(request):
    products = list(Product.objects.all().values())
    return JsonResponse(products, safe=False)


@login_required
def customer_edit(request, customer_id):
    customer_obj = get_object_or_404(Customer, id=customer_id)
    if request.method == "POST":
        customer_form = CustomerForm(request.POST, instance=customer_obj)
        if customer_form.is_valid():
            new_customer = customer_form.save()
            return redirect('customers')
    context = {}
    context['customer_form'] = CustomerForm(instance=customer_obj)
    return render(request, 'gstbillingapp/customer_edit.html', context)


@login_required
def customer_delete(request):
    if request.method == "POST":
        customer_id = request.POST["customer_id"]
        customer_obj = get_object_or_404(Customer, id=customer_id)
        customer_obj.delete()
    return redirect('customers')


@login_required
def customer_add(request):
    if request.method == "POST":
        customer_form = CustomerForm(request.POST)
        new_customer = customer_form.save(commit=False)
        new_customer.save()
        # create customer book
        return redirect('customers')
    context = {}
    context['customer_form'] = CustomerForm()
    return render(request, 'gstbillingapp/customer_edit.html', context)


@login_required
def product_edit(request, product_id):
    product_obj = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        product_form = ProductForm(request.POST, instance=product_obj)
        if product_form.is_valid():
            new_product = product_form.save()
            return redirect('products')
    context = {}
    context['product_form'] = ProductForm(instance=product_obj)
    return render(request, 'gstbillingapp/product_edit.html', context)


@login_required
def product_add(request):
    if request.method == "POST":
        product_form = ProductForm(request.POST)
        if product_form.is_valid():
            new_product = product_form.save(commit=False)
            new_product.save()

            return redirect('products')
    context = {}
    context['product_form'] = ProductForm()
    return render(request, 'gstbillingapp/product_edit.html', context)


@login_required
def product_delete(request):
    if request.method == "POST":
        product_id = request.POST["product_id"]
        product_obj = get_object_or_404(Product, id=product_id)
        product_obj.delete()
    return redirect('products')





# ================= Static Pages ==============================

def landing_page(request):
    context = {}
    return render(request, 'gstbillingapp/pages/landing_page.html', context)
