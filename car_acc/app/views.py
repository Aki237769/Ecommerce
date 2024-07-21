from django.shortcuts import render,redirect, HttpResponse,get_object_or_404
from django.contrib.auth.hashers import make_password,check_password
from django.db import IntegrityError
from django.views.decorators.http import require_POST
from . import models 

# Create your views here.


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

def home(request):
    return render(request,"home.html")

def about(request):
    return render(request, "about.html")

def admin_update(request):

    if not(request.session.get('admin_id')):
        return redirect('login')
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        if all([name,email,phone]):
            try:
                admin=models.Admin_data.objects.get(admin_id=request.session.get('admin_id'))
                admin.admin_name=name
                admin.admin_email=email
                admin.admin_phone=phone
                admin.save()
                data={
                    "admin_data":admin,
                    "success":"done"
                }
                return render(request, "admin/admin_update.html",context=data)
            except IntegrityError as e:
                if'admin_phone'in str(e):
                    error={
                        'error':'phone-error'
                    }
                else:
                    error={
                        'error':'email-error'
                    }
        else:
            error={
                'error':'empty-fields'
            }
        return render(request, "admin/admin_update.html", context=error)
               
    admin_data=models.Admin_data.objects.get(admin_id=request.session.get('admin_id'))
    data={
        'admin_data':admin_data
    }
    return render(request,"admin/admin_update.html", context=data)


def order_view(request,order_id,item_id):
    if not(request.session.get('admin_id')):
         return redirect('login')
    if request.method=="POST":
        order=get_object_or_404(models.Order,id=order_id)
        item = models.Order_Item.objects.get(id=item_id)
        answer = request.POST.get('status')
        print(answer)
        if answer:
            if answer == "Yes":
                item.is_delivered = True
                item.save()
            else :
                item.is_delivered = False
                item.save()
        
    order=get_object_or_404(models.Order,id=order_id)
    item=models.Order_Item.objects.filter(order_id=order.id)

    data={
        'orders':order,
        'products':item
    }
    
    return render(request, "admin/order_view.html",context=data)
# def del_status(request,item_id):
#     if not (request.session.get('admin_id')):
#         return redirect('login')
#     if request.method=="POST":

#         order=get_object_or_404(models.Order,id=order_id)
#         product=models.Order_Item.objects.filter(order_id=order.id)

#     data={
#         'orders':order,
#         'products':item
#     }
#         item = models.Order_Item.objects.filter(id=item_id)
#         answer = request.session.get('status')
#         if answer:
#             if answer == "Yes":
#                 item.is_delivered = True
#                 item.save()
#                 return render(request, "admin/order_view.html",context=data)
#             else :
#                 item.is_delivered = False
#                 item.save()
#                 return render(request, "admin/order_view.html",context=data)
        

def customer_view(request):
    if not(request.session.get('admin_id')):
        return redirect('login')
    customer_order=models.Order.objects.all()
    data={
        'orders':customer_order
    }
    return render(request, "admin/customer_order.html",context=data)





def admin(request):
    if not(request.session.get('admin_id')):
        return redirect("login")
    admin_data=models.Admin_data.objects.get(admin_id=request.session.get('admin_id'))
    data={
        'admin_data':admin_data
    }
    return render(request, "admin/admin.html",context=data)


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





def customerpage(request):
    if not(request.session.get('customer_id')):
        return redirect("login")
    customer_data=models.Customer_data.objects.get(customer_id=request.session.get('customer_id'))
    data={
        'customer_data':customer_data
    }
    return render(request, "customer/customer.html", context=data)

def update_profile(request):
    if not(request.session.get('customer_id')):
        return redirect('login')
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        address=request.POST.get('address') 
        if all([name,email,phone,address]):
            try:
                customer=models.Customer_data.objects.get(customer_id=request.session.get('customer_id'))
                customer.customer_name=name
                customer.customer_email=email
                customer.customer_phone=phone
                customer.customer_address=address
                customer.save()
                data={
                    "customer_data":customer,
                    "success":"done"
                }
                return render(request, 'customer/customer.html',context=data)
            except IntegrityError as e:
                if'customer_phone'in str(e):
                    error={
                        'error':'phone-error'
                    }
                else:
                    error={
                        'error':'email-error'
                    }
        else:
            error={
                'error':'empty-fields'
            }
        return render(request, 'customer/profile_update.html', context=error)
               
    customer_data=models.Customer_data.objects.get(customer_id=request.session.get('customer_id'))
    data={
        'customer_data':customer_data
    }
    return render(request,"customer/profile_update.html", context=data)
    


def handle_product_action(request, product_id):
    if not(request.session.get('customer_id')):
        return redirect('login')
    if request.method == 'POST':
        customer = models.Customer_data.objects.get(customer_id=request.session['customer_id'])
        product = get_object_or_404 (models.Product_data, product_id=product_id)
        quantity = int(request.POST.get('quantity', 1))
        action = request.POST.get('action')

        if action == 'add_to_cart':
            cart_item, created = models.Cart.objects.get_or_create(customer=customer, product=product)
            if not created:
                if cart_item.quantity<5:
                    cart_item.quantity += quantity
                else:
                    cart_item.quantity=5
            else:
                if cart_item.quantity<5:
                    cart_item.quantity = quantity
                else:
                    cart_item.quantity=5
            cart_item.save()
            return redirect('cart')  # Redirect to the cart page

        elif action == 'buy_now':
            cart_item, created = models.Cart.objects.get_or_create(customer=customer, product=product)
            if not created:
                if cart_item.quantity<5:
                    cart_item.quantity += quantity
                else:
                    cart_item.quantity=5
            else:
                if cart_item.quantity<5:
                    cart_item.quantity = quantity
                else:
                    cart_item.quantity=5
            cart_item.save()  # Clear existing cart items
            request.session['single_product'] = True
            request.session['single_product_id'] = product.product_id
            return redirect('address')  # Redirect to the checkout page

    return redirect('cart')  # Redirect to the homepage or any other appropriate page



def cart(request):
    if not(request.session.get("customer_id")):
        return redirect("login")
    if request.method == 'POST':
        customer = models.Customer_data.objects.get(customer_id=request.session['customer_id'])
        product_ids = request.POST.getlist('product_id')
        for product_id in product_ids:
            quantity_key = f'quantity_{product_id}'
            quantity = int(request.POST.get(quantity_key))
            product = models.Product_data.objects.get(product_id=product_id)
            
            # Update the cart item with the new quantity
            cart_item, created = models.Cart.objects.get_or_create(customer=customer, product=product)
            cart_item.quantity = int(quantity)  # Ensure quantity is saved as an integer
            cart_item.save()
        data = {
            'customer_data': customer
        }
        return render(request,'customer/address.html',context=data)
    product=models.Cart.objects.filter(customer=request.session.get('customer_id'))
    total_price = round(sum(item.product.product_price * item.quantity for item in product))
    quantity_range = range(1,6)
    data={
        "product_data": product,
        "total_price":total_price,
        "quantity_range":quantity_range

    }
    return render(request, 'customer/cart.html',context=data)

def remove_cart_item(request,product_id):
    if not(request.session.get('customer_id')):
        return redirect('login')
    product_cart=models.Cart.objects.get(id=product_id)
    product_cart.delete()
    product=models.Cart.objects.filter(customer=request.session.get('customer_id'))
    data={
        "product_data": product
    }
    return render(request,'customer/cart.html', context=data)
    
    


def address(request):
    if not (request.session.get('customer_id')):
        return redirect('login')
    customer = models.Customer_data.objects.get(customer_id=request.session.get('customer_id'))
    data = {
        'customer_data' : customer
    }
    return render(request, 'customer/address.html',context=data)


def update_address(request):
    if not (request.session.get('customer_id')):
        return redirect('login')
    if request.method=="POST":
        address=request.POST.get('address')
        try:
            customer=models.Customer_data.objects.get(customer_id=request.session.get('customer_id'))
            customer.customer_address=address
            customer.save()
            data={
                "customer_data":customer,
                "success":"done"
            }
            return render(request, 'customer/address.html',context=data)
        except:
            error = {
                'error':'not-updated'
            }
            return render(request,"customer/update_address",context=error)
    customer = models.Customer_data.objects.get(customer_id=request.session.get('customer_id'))
    data = {
        'customer_data' : customer
    }
    return render(request, 'customer/updateaddress.html',context=data)

def checkout(request):
    if not(request.session.get("customer_id")):
        return redirect('login')
    single_product = request.session.get('single_product', False)
    product_id = request.session.get('single_product_id', None)
    if single_product and product_id:
        cart_items = models.Cart.objects.filter(customer=request.session.get('customer_id'), product_id=product_id)
    else:
        cart_items = models.Cart.objects.filter(customer=request.session.get('customer_id'))
    if request.method=="POST":
        total_price = round(sum(item.product.product_price * item.quantity for item in cart_items)) 
        payment_method=request.POST.get("payment")
        if payment_method=="netbanking":
            return render(request, 'customer/netbanking.html')
        
        elif payment_method=="cod" :
            customer = models.Customer_data.objects.get(customer_id=request.session['customer_id'])
            order = models.Order.objects.create(customer=customer, total_amount = total_price, address = customer.customer_address)
            for item in cart_items:
                models.Order_Item.objects.create(customer=customer, order = order, product = item.product, quantity = item.quantity, price = item.product.product_price)
            if single_product and product_id:
                cart_items.delete()
            else:
                models.Cart.objects.filter(customer = customer).delete()

        request.session['single_product'] = False
        request.session['single_product_id'] = None
        order = get_object_or_404(models.Order, id = order.id)
        items = models.Order_Item.objects.filter(order_id=order.id)
        data = {
            'order' : order,
            'products' : items
        }
        return render(request, 'customer/orderconfirmation.html', context=data)

    return render(request,'customer/checkout.html')

def orderconfirmation(request):
    if not (request.session.get('customer_id')):
        return redirect('login')
    order=get_object_or_404(models.Order,id=order.id)
    data={
        "order":order
    }
    return render(request, 'customer/orderconfirmation.html',context=data)


def orderhistory(request):
    if not(request.session.get("customer_id")):
            return redirect("login")  
        
    order = models.Order.objects.filter(customer_id = request.session.get('customer_id'))
    items = models.Order_Item.objects.filter(customer_id = request.session.get('customer_id'))

    for item in items:
        item.total_price = item.quantity * item.price
    
    data = {
            'order' : order,
            'products' : items
    }
    return render(request, "customer/orderhistory.html",context=data)                           



def netbanking(request):
    if not(request.session.get("customer_id")):
            return redirect("login")  


    return render(request, "customer/netbanking.html")




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


        if all([email,password,user]):
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
    



