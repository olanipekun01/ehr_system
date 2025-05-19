from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Department)
admin.site.register(Items)
admin.site.register(Disbursement)
admin.site.register(DisbursementItem)
admin.site.register(Supplier)
