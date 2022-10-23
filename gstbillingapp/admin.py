from django.contrib import admin

# Register your models here.
from .models import Customer, Financial_year, Place_of_supply, Transporter_info, Vehicle
from .models import Invoice
from .models import Product
from .models import UserProfile

admin.site.register(UserProfile)

admin.site.register(Customer)
admin.site.register(Invoice)
admin.site.register(Product)
admin.site.register(Financial_year)
admin.site.register(Vehicle)
admin.site.register(Place_of_supply)
admin.site.register(Transporter_info)
