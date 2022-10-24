from email.policy import default
from django.db import models
from django.contrib.auth.models import User

from datetime import datetime
# Create your models here.



# ======================= Invoice Data models =================================

class Customer(models.Model):
    customer_name = models.CharField(max_length=200)
    customer_address = models.TextField(max_length=600, blank=True, null=True)
    customer_gst = models.CharField(max_length=15, blank=True, null=True)
    def __str__(self):
        return self.customer_name

class Place_of_supply(models.Model):
    state=models.CharField(max_length=100)
    code=models.CharField(max_length=100)
    def __str__(self):
        return self.state + " / " + self.code

class Financial_year(models.Model):
    year=models.CharField(max_length=50)
    def __str__(self):
        return self.year

class Transporter_info(models.Model):
    transporter=models.CharField(max_length=150)
    def __str__(self):
        return self.transporter

class Payment_terms(models.Model):
    payment_term=models.CharField(max_length=150)
    def __str__(self):
        return self.payment_term

class Vehicle(models.Model):
    name= models.CharField(max_length=100)
    vehicle_number = models.CharField(max_length=100)
    def __str__(self):
        return self.name +" | "+ self.vehicle_number

class Invoice(models.Model):
    invoice_number = models.IntegerField()
    invoice_date = models.DateField()
    order_date = models.DateField(default=datetime.now())
    
    invoice_customer = models.ForeignKey(
        'Customer',
        on_delete=models.SET_NULL,
        null=True
    )
    invoice_json = models.TextField()
    
    def __str__(self):
        return str(self.invoice_number) + " | " + str(self.invoice_date)


class Product(models.Model):
    item_code = models.CharField(max_length=200,null=True, default="-")
    product_name = models.CharField(max_length=200)
    product_hsn = models.CharField(max_length=50, null=True, blank=True)
    product_unit = models.CharField(max_length=50)
    product_rate = models.FloatField()
    def __str__(self):
        return str(self.product_name)

