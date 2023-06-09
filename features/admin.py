from django.contrib import admin
from .models import FeedbackTable, SupplierRecord, delivery
# Register your models here.

admin.site.register(FeedbackTable)
admin.site.register(SupplierRecord)
admin.site.register(delivery)