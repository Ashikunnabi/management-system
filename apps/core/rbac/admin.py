from django.contrib import admin

from .models import *


admin.site.register(Permission)
admin.site.register(Role)
admin.site.register(User)
admin.site.register(Client)
admin.site.register(Feature)
admin.site.register(ActivityLog)
admin.site.register(Department)
admin.site.register(Branch)