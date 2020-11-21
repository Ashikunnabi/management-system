from django.contrib import admin
from .models import *
admin.site.register(Category)
admin.site.register(Vendor)
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Buy)
admin.site.register(Sell)
admin.site.register(Transfer)

# Register your models here.
