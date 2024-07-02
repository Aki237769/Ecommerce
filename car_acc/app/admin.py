from django.contrib import admin
from .import models

# Register your models here.

admin.site.register(models.Admin_data)
admin.site.register(models.Customer_data)
admin.site.register(models.Product_data)