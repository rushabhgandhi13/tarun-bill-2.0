from django.forms import ModelForm
from .models import Customer
from .models import Product


class CustomerForm(ModelForm):
     class Meta:
         model = Customer
         fields = ['customer_name', 'customer_address', 'customer_gst']


class ProductForm(ModelForm):
     class Meta:
         model = Product
         fields = ['product_name','item_code', 'product_hsn', 'product_unit', 'product_rate']


# class UserProfileForm(ModelForm):
#     def __init__(self, *args, **kwargs):
#         # first call parent's constructor
#         super(UserProfileForm, self).__init__(*args, **kwargs)
#         # there's a `fields` property now
#         self.fields['business_title'].required = True

#     class Meta:
#         model = UserProfile
#         fields = ['business_title', 'business_address', 'business_email', 'business_phone', 'business_gst']

