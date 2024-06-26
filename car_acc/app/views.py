from django.shortcuts import render,redirect
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
    return render(request, "carinterior.html")

def carexterior(request):
    return render(request, "carexterior.html")

def carcare(request):
    return render(request, "carcare.html")

def carstyling(request):
    return render(request, "carstyling.html")

def bulkdiscount(request):
    return render(request, "bulkdiscount.html")

def returnpolicy(request):
    return render(request, "returnpolicy.html" )

def contactus(request):
    return render(request, "contactus.html")

def signup(request):
    if request.POST:
        name=request.POST['name']
        email=request.POST['email']
        password=request.POST['password']
        confirmpassword=request.POST['confirmpassword']
        gender=request.POST['gender']
        role=request.POST['role']
        phonenumber=request.POST
        if all([name,email,password,confirmpassword,gender,role,phonenumber]):
            if role=="Seller":
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
                        request.session['id'] = customer.customer_id
                        request.session['name'] = customer.customer_name
                        request.session['user'] = user
                        print(user)
                        return redirect('home')
                    
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
                        request.session['id'] = admin.admin_id
                        request.session['name'] = admin.admin_name
                        request.session['user'] = user
                        print(user)
                        return redirect('home')
                    
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
        request.session.pop('id')
        request.session.pop('name')
        request.session.pop('user')
        return redirect('login')
    



