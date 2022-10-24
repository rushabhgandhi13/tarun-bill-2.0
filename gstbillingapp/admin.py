from django.contrib import admin

# Register your models here.
from .models import Customer, Financial_year, Payment_terms, Place_of_supply, Transporter_info, Vehicle
from .models import Invoice
from .models import Product


admin.site.register(Customer)
admin.site.register(Invoice)
admin.site.register(Product)
admin.site.register(Financial_year)
admin.site.register(Vehicle)
admin.site.register(Place_of_supply)
admin.site.register(Transporter_info)
admin.site.register(Payment_terms)
