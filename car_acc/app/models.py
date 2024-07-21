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
    customer_address=models.TextField(null=True)

    def __str__(self) -> str:
        return f"customer_ID : {self.customer_id}, customer_Name : {self.customer_name}"

class Product_data(models.Model):
    product_id=models.AutoField(primary_key=True, unique=True)
    product_category=models.CharField(max_length=20)
    product_name= models.CharField(max_length=100)
    product_description=models.CharField(max_length=200)
    product_price=models.FloatField()
    product_image=models.ImageField(upload_to='productimage/',null=True,blank=True)
    
    def __str__(self) -> str:
        return f"Product_ID : {self.product_id}, Product_name : {self.product_name}"

class Cart(models.Model):
    customer=models.ForeignKey(Customer_data,related_name='customer', on_delete=models.CASCADE)
    product=models.ForeignKey(Product_data,related_name='product', on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)

    def __str__(self) -> str:
        return f"product : {self.product.product_name}, quantity : {self.quantity}"




class Order(models.Model):
    customer=models.ForeignKey(Customer_data, on_delete=models.CASCADE)
    total_amount=models.DecimalField(max_digits=10,decimal_places=2,null=True)
    order_date=models.DateTimeField(auto_now_add=True)
    address = models.TextField(null=True)

    def _str_(self) -> str:
        return f"order_by: {self.customer.customer_name}, product : {self.product.product_name}"
    

class Order_Item(models.Model):
    customer = models.ForeignKey(Customer_data, on_delete=models.CASCADE)
    order = models.ForeignKey(Order,related_name='items',on_delete=models.CASCADE)
    product = models.ForeignKey(Product_data,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_delivered = models.BooleanField(default=False)

    






