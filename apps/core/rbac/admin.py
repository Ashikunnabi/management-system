from django.contrib import admin

from .models import *


admin.site.register(Permission)
admin.site.register(Role)
admin.site.register(User)
admin.site.register(Customer)
admin.site.register(Feature)