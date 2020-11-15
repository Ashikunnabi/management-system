import uuid
from django.db import models
from django.core.validators import RegexValidator
from apps.core.rbac.models import AuditTrail, Department, Group, User


class Category(AuditTrail):
    name = models.CharField(max_length=100,
                            blank=False,
                            null=False,
                            validators=[RegexValidator(
                                regex='[-a-zA-Z0-9_.\s]{2,100}$',
                                message='Category contains alphanumeric, underscore, space and period(.). Length: 2 to 100'
                            )]
                            )
    department = models.ForeignKey(Department, on_delete=models.CASCADE)


class Vendor(AuditTrail):
    name = models.CharField(max_length=100,
                            blank=False,
                            null=False,
                            validators=[RegexValidator(
                                regex='[-a-zA-Z0-9_.\s]{2,100}$',
                                message='Vendor contains alphanumeric, underscore, space and period(.). Length: 2 to 100'
                            )]
                            )
    mobile = models.CharField(max_length=12)
    address = models.CharField(max_length=500)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Product(AuditTrail):
    name = models.CharField(max_length=100,
                            blank=False,
                            null=False,
                            validators=[RegexValidator(
                                regex='[-a-zA-Z0-9_.\s]{2,100}$',
                                message='Product contains alphanumeric, underscore, space and period(.). Length: 2 to 100'
                            )]
                            )
    code = models.CharField(max_length=10, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    box_number = models.CharField(max_length=50, null=True, blank=True)
    physical_location = models.CharField(max_length=50, null=True, blank=True)
    extra_description = models.TextField()  # color=red\nsize=35\nweight=500gm
    unit_price = models.FloatField(default=00.00)
    available_stock = models.IntegerField()
    safety_stock_limit = models.IntegerField()
 

class Customer(AuditTrail):
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=14)
    email = models.EmailField()
    address = models.TextField()
    profession = models.CharField(max_length=50)
    organization_name = models.CharField(max_length=50)
    organization_address = models.TextField()
 

class Buy(AuditTrail):
    product = models.ForeignKey(Product, blank=False, on_delete=models.CASCADE)
    bought_by = models.ForeignKey(User, blank=False, on_delete=models.CASCADE)
    document = models.FileField(upload_to='inventory/document/buy/%Y/%m/%d', blank=True, null=True)
    quantity = models.IntegerField()
    unit_price = models.FloatField(default=00.00)
    price_changed = models.BooleanField(default=False)  # set True when existing product unit price changed
    comment = models.TextField()  # make the field mandatory if price_changed=True
    
    
class Sell(AuditTrail):
    TYPE = (
        (1, 'Full Payment'),
        (2, 'EMI'),
        (3, 'Discount'),
        (4, 'Full Free'),
    )
    invoice_no = models.CharField(default=uuid.uuid4().hex[:8])
    purchase_type = models.IntegerField(choices=TYPE, blank=False, null=False)
    product = models.ManyToManyField(Product, blank=False)
    product_details = models.TextField(blank=False, null=False)  # all product information in JSON
    customer = models.ForeignKey(Customer, blank=False, on_delete=models.Protect)
    quantity = models.TextField(blank=False, null=False)  # total quantity in list 
    actual_price = models.FloatField(blank=False, null=False)  # price before adding (vat+service_charge)-discount
    vat = models.FloatField()  # vat will be in percentage
    service_charge = models.FloatField()  # service_charge will be in percentage
    discount = models.IntegerField(blank=True, null=True) # discount will be in percentage
    total_price = models.FloatField(blank=False, null=False)  # price after adding (vat+service_charge)-discount
    paid_price = models.FloatField(blank=False, null=False)  # price that customer paid    
    emi_tenor_month = models.IntegerField(blank=True, null=True)  # how many month customer will pay to complete full payment
    emi_tenor_month_paid = models.IntegerField(blank=True, null=True)  # how many month customer paid money to complete full payment
    emi_tenor_monthly_ammount = models.FloatField(blank=True, null=True)  # how much money per month customer will pay to complete full payment
    payment_history = models.TextField(blank=True, null=True)  # list of dates when customer paid to complete full payment
    payment_gateway_information = models.TextField()
    other_information = models.TextField()
    
    
class Transfer(AuditTrail):
    invoice_no = models.CharField(default=uuid.uuid4().hex[:8])
    product = models.ForeignKey(Product, blank=False, on_delete=models.CASCADE)
    product_details = models.TextField(blank=False, null=False)  # all product information in JSON
    quantity = models.IntegerField(blank=False, null=False)
    department =  models.ForeignKey(Department, blank=False, on_delete=models.CASCADE)
    other_information = models.TextField()
    



