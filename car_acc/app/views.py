from django.shortcuts import render,redirect, HttpResponse,get_object_or_404
from django.contrib.auth.hashers import make_password,check_password
from django.db import IntegrityError

from . import models 

# Create your views here.

def home(request):
    return render(request,"home.html")

# def navbar(request):
#     return render(request, "app/navbar.html")
def about(request):
    return render(request, "about.html")

def carinterior(request):
    car_int_product= models.Product_data.objects.filter(product_category='car_interior' )
    data={
        "interior_product":car_int_product

    }
    return render(request, "carinterior.html", context=data)

def carexterior(request):
    car_ext_product=models.Product_data.objects.filter(product_category='car_exterior')
    data={
        "exterior_product":car_ext_product
    }
    return render(request, "carexterior.html", context=data)

def carcare(request):
    car_care_product=models.Product_data.objects.filter(product_category='car_care')
    data={
        "care_product":car_care_product
    }
    return render(request, "carcare.html", context=data)

def carstyling(request):
    car_style_product=models.Product_data.objects.filter(product_category='car_styling')
    data={
        "styling_product":car_style_product
    }
    return render(request, "carstyling.html", context=data)

def bulkdiscount(request):
    return render(request, "bulkdiscount.html")

def returnpolicy(request):
    return render(request, "returnpolicy.html" )

def contactus(request):
    return render(request, "contactus.html")
def product_add(request):

    if request.method == 'POST':
        product_category = request.POST['product_category']
        product_name = request.POST['product_name']
        product_description = request.POST['product_description']
        product_price = request.POST['product_price']
        
        if all([product_category,product_name,product_description,product_price]):
            try:
                
                new_product=models.Product_data.objects.create(   
                product_category=product_category,
                product_name=product_name,
                product_description=product_description,
                product_price=product_price)
                if request.FILES.get('product_image'):
                    
                    product_image = request.FILES.get('product_image')
                    new_product.prdouct_image=product_image
                    new_product.save()
                return HttpResponse('success')
            except:
                return HttpResponse("data not updated")
                                    
        
        
        return redirect('success') 
    return render(request, "admin/product.html")




def admin(request):
    if not(request.session.get('admin_id')):
        return redirect("login")
    admin_data=models.Admin_data.objects.get(admin_id=request.session.get('admin_id'))
    data={
        'admin_data':admin_data
    }
    return render(request, "admin/admin.html",context=data)

def customerpage(request):
    if not(request.session.get('customer_id')):
        return redirect("login")
    customer_data=models.Customer_data.objects.get(customer_id=request.session.get('customer_id'))
    data={
        'customer_data':customer_data
    }
    return render(request, "customer/customer.html", context=data)

def buynow(request):
    if not(request.session.get('customer_id')):
        return redirect('login')
    product = get_object_or_404(models.Product_data, product_id=request.session.get("product_id"))
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        order=models.Order.objects.create(customer=request.session.get("customer_id"), product=product, quantity=quantity)
        
        return redirect('order_confirmation', order_id=order.id)
    return render(request, 'orderhistory.html',{'product':product})
    

def orderhistory(request):
    
    return render(request, "customer/orderhistory.html")

def add_to_cart(request):
    if not(request.session.get('customer_id')):
        return redirect('login')
    if request.method=="POST":
        customer_id=models.Customer_data.objects.get(customer=request.session.get('customer_id'))
        product_key=request.POST.get('product_id')
        product_name=get_object_or_404(models.Product_data,product_id=product_key)
        product_quantity=request.POST.get('product_quantity')
        models.Cart.objects.create(customer=customer_id,product=product_name,quantity=product_quantity)
        return redirect('cart')
    

      
          
      
    return render(request, "customer/cart.html")


def signup(request):
    if request.POST:
        name=request.POST['name']
        email=request.POST['email']
        password=request.POST['password']
        confirmpassword=request.POST['confirmpassword']
        gender=request.POST['gender']
        role=request.POST['role']
        phonenumber=request.POST['phone']
        if all([name,email,password,confirmpassword,gender,role,phonenumber]):
            if role=="Seller" and models.Admin_data.objects.filter(admin_role__iexact='Seller').exists():
                error={'error':'seller exist'}
            elif role=='Seller':
                
                if password == confirmpassword:
                    encrypt_password= make_password(password)
                    try:
                        models.Admin_data.objects.create(admin_name=name,
                                                         admin_email=email,
                                                         admin_password=encrypt_password,
                                                         admin_gender=gender,
                                                         admin_role=role,
                                                         admin_phone=phonenumber)
                        return render(request,'signup.html', context={'success':'done'})
                    except IntegrityError as e:
                        if'admin_phone'in str(e):
                            error={
                                'error':'Phone-error'
                            }
                        else:
                            error={
                                'error':'email-error'
                            }
                else:
                    error={
                        'error':'password-mismatch'
                    }
                return render(request, 'signup.html', context=error)    
            
            elif role=="Customer":
                if password == confirmpassword:
                    encrypt_password= make_password(password)
                    try:
                        models.Customer_data.objects.create(customer_name=name,
                                                         customer_email=email,
                                                         customer_password=encrypt_password,
                                                         customer_gender=gender,
                                                         customer_role=role,
                                                         customer_phone=phonenumber)
                        return render(request,'signup.html', context={'success':'done'})
                    except IntegrityError as e:
                        if'customer_phone'in str(e):
                            error={
                                'error':'Phone-error'
                            }
                        else:
                            error={
                                'error':'email-error'
                            }
                else:
                    error={
                        'error':'password-mismatch'
                    }
        else:
                error={
                    'error':'empty-fields'
                }
        return render(request, 'signup.html', context=error)    
    return render(request, "signup.html")

def login(request):
    if request.POST:
        email=request.POST.get('email')
        password=request.POST.get('password')

        if models.Customer_data.objects.filter(customer_email=email).exists():
            user="customer"
        elif models.Admin_data.objects.filter(admin_email=email).exists():
            user="admin"


        if all([[email,password,user]]):
            if user=="customer":
                check_email = models.Customer_data.objects.filter(customer_email=email).exists()
                if check_email:
                    customer = models.Customer_data.objects.get(customer_email=email)
                    check_pass = check_password(password,customer.customer_password)
                    if check_pass:
                        request.session['customer_id'] = customer.customer_id
                        request.session['customer_name'] = customer.customer_name
                        request.session['customer_role'] = user
                    
                        return redirect('customer')
                    
                    else:
                        error = {
                            'error' : 'not-matched'
                        }
                else:
                    error = {
                        'error': 'not-matched'
                    }
            elif user=="admin":
                check_email = models.Admin_data.objects.filter(admin_email=email).exists()
                if check_email:
                    admin = models.Admin_data.objects.get(admin_email=email)
                    check_pass = check_password(password,admin.admin_password)
                    if check_pass:
                        request.session['admin_id'] = admin.admin_id
                        request.session['admin_name'] = admin.admin_name
                        request.session['admin_role'] = user
                        return redirect('admin_dashboard')
                    
                    else:
                        error = {
                            'error' : 'not-matched'
                        }
                else:
                    error = {
                        'error': 'not-matched'
                    }
        else:
            error = {
                'error' : 'empty-fields'
            }
                
        return render(request, 'login.html',context=error)
    
    return render(request, "login.html")


            

def logout(request):
        if 'customer_role' in request.session:
            request.session.pop('customer_id', )
            request.session.pop('customer_name')
            request.session.pop('customer_role')
        elif 'admin_role' in request.session:
            request.session.pop('admin_id')
            request.session.pop('admin_name')
            request.session.pop('admin_role')


        return redirect('login')
    



