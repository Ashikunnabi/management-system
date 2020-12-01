from django.db import models
from django.core.validators import RegexValidator
from apps.core.rbac.models import AuditTrail, Department
from apps.core.base.utils.custom_validators import name_validator, mobile_validator
from apps.core.base.utils.basic import random_hex_code


class Category(AuditTrail):
    name = models.CharField(max_length=100,
                            blank=False,
                            null=False,
                            unique=True,
                            validators=[RegexValidator(regex=name_validator()[0], message=name_validator()[1])])
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='category_department')

    def __str__(self):
        return f"{self.name} ({self.parent.name if self.parent else self.department})"

    def total_product(self):
        return Product.objects.filter(category=self).count()


class Vendor(AuditTrail):
    name = models.CharField(max_length=100,
                            blank=False,
                            null=False,
                            validators=[RegexValidator(regex=name_validator()[0], message=name_validator()[1])]
                            )
    mobile = models.CharField(max_length=14,
                              validators=[RegexValidator(regex=mobile_validator()[0], message=mobile_validator()[1])])
    address = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='vendor_category')

    def __str__(self):
        return f"{self.name} ({self.category.name})"

    class Meta:
        unique_together = ('name', 'category')


class UnitType(AuditTrail):
    name = models.CharField(max_length=100,
                            blank=False,
                            null=False,
                            unique=True,
                            validators=[RegexValidator(regex=name_validator()[0], message=name_validator()[1])]
                            )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True,
                                 related_name='unit_type_category')

    def __str__(self):
        return self.name


class Product(AuditTrail):
    name = models.CharField(max_length=100,
                            blank=False,
                            null=False,
                            unique=True,
                            validators=[RegexValidator(regex=name_validator()[0], message=name_validator()[1])]
                            )
    code = models.CharField(max_length=10, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product_category')
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='product_vendor')
    box_number = models.CharField(max_length=50, null=True, blank=True)
    physical_location = models.CharField(max_length=50, null=True, blank=True)
    extra_description = models.TextField()  # color=red\nsize=35\nweight=500gm
    unit_type = models.ForeignKey(UnitType, on_delete=models.PROTECT, related_name='product_unit_type')
    unit_price = models.FloatField(default=00.00)
    lowest_selling_price = models.FloatField(default=00.00)
    available_stock = models.IntegerField()
    safety_stock_limit = models.IntegerField()

    def __str__(self):
        return f'{self.name} ({self.code})'


class Customer(AuditTrail):
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=14,
                              validators=[RegexValidator(regex=mobile_validator()[0], message=mobile_validator()[1])])
    email = models.EmailField()
    address = models.TextField()
    profession = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Buy(AuditTrail):
    product = models.ForeignKey(Product, blank=False, on_delete=models.CASCADE, related_name='buy_product')
    bought_by = models.ForeignKey(Customer, blank=False, on_delete=models.CASCADE, related_name='buy_customer')
    document = models.FileField(upload_to='inventory/document/buy/%Y/%m/%d', blank=True, null=True)
    quantity = models.IntegerField()
    unit_price = models.FloatField(default=00.00)
    price_changed = models.BooleanField(default=False)  # set True when existing product unit price changed
    comment = models.TextField()  # make the field mandatory if price_changed=True

    def __str__(self):
        return f"{self.product}: {self.bought_by}"


class Sell(AuditTrail):
    TYPE = (
        (1, 'Full Payment'),
        (2, 'EMI'),
        (3, 'Discount'),
        (4, 'Full Free'),
    )
    invoice_no = models.CharField(max_length=8, default=random_hex_code)
    purchase_type = models.IntegerField(choices=TYPE, blank=False, null=False)
    product = models.ManyToManyField(Product, blank=False)
    product_details = models.TextField(blank=False, null=False)  # all product information in JSON
    customer = models.ForeignKey(Customer, blank=False, on_delete=models.CASCADE, related_name='sell_customer')
    quantity = models.TextField(blank=False, null=False)  # total quantity in list/dictionary
    actual_price = models.FloatField(blank=False, null=False)  # price before adding (vat+service_charge)-discount
    vat = models.FloatField()  # vat will be in percentage
    service_charge = models.FloatField()  # service_charge will be in percentage
    discount = models.IntegerField(blank=True, null=True)  # discount will be in percentage
    total_price = models.FloatField(blank=False, null=False)  # price after adding (vat+service_charge)-discount
    paid_price = models.FloatField(blank=False, null=False)  # price that customer paid
    emi_tenor_month = models.IntegerField(blank=True,
                                          null=True)  # how many month customer will pay to complete full payment
    emi_tenor_month_paid = models.IntegerField(blank=True,
                                               null=True)  # how many month customer paid money to complete full payment
    emi_tenor_monthly_amount = models.FloatField(blank=True,
                                                 null=True)  # how much money per month customer will pay to complete full payment
    payment_history = models.TextField(blank=True,
                                       null=True)  # list of dates when customer paid to complete full payment
    payment_gateway_information = models.TextField()
    other_information = models.TextField()


class Transfer(AuditTrail):
    invoice_no = models.CharField(max_length=8, default=random_hex_code)
    product = models.ForeignKey(Product, blank=False, on_delete=models.CASCADE, related_name='transfer_product')
    product_details = models.TextField(blank=False, null=False)  # all product information in JSON
    quantity = models.IntegerField(blank=False, null=False)
    department = models.ForeignKey(Department, blank=False, on_delete=models.CASCADE, related_name='transfer_department')
    other_information = models.TextField()


