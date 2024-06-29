from django.db import models
from .import views


class Admin_data(models.Model):
    admin_id=models.AutoField(primary_key=True, unique=True)
    admin_name=models.CharField(max_length=100)
    admin_email=models.EmailField(max_length=100)
    admin_password=models.CharField(max_length=20)
    admin_gender=models.CharField(max_length=10)
    admin_role=models.CharField(max_length=20)
    admin_phone=models.CharField(max_length=10)

    def __str__(self) -> str:
        return f"Admin_ID : {self.admin_id}, Admin_Name : {self.admin_name}"


class Customer_data(models.Model):
    customer_id=models.AutoField(primary_key=True, unique=True)
    customer_name=models.CharField(max_length=100)
    customer_email=models.EmailField(max_length=100)
    customer_password=models.CharField(max_length=20)
    customer_gender=models.CharField(max_length=10)
    customer_role=models.CharField(max_length=20)
    customer_phone=models.CharField(max_length=10)

    def __str__(self) -> str:
        return f"customer_ID : {self.customer_id}, customer_Name : {self.customer_name}"

class Product_data(models.Model):
    product_id=models.AutoField(primary_key=True, unique=True)
    product_category=models.CharField(max_length=20)
    product_name= models.CharField(max_length=100)
    product_description=models.CharField(max_length=200)
    product_price=models.FloatField()
    prdouct_image=models.ImageField(upload_to='productimage/',null=True,blank=True)
    
    def __str__(self) -> str:
        return f"Product_ID : {self.product_id}, Product_name : {self.product_name}"






