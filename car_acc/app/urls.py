from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('',views.home, name='home'),
    path('about/',views.about, name='about'),
    path('carinterior/',views.carinterior, name='carint'),
    path('carexterior/',views.carexterior, name='carext'),
    path('carcare/' ,views.carcare, name= 'carcare'),
    path('carstyling/' , views.carstyling, name='carstyling'),
    path('bulkdiscount/', views.bulkdiscount, name='bulkdiscount'),
    path('returnpolicy/' , views.returnpolicy, name= 'returnpolicy'),
    path('contactus/', views.contactus, name='contactus' ),
    path('signup/', views.signup, name='signup' ),
    path('login/', views.login, name='login' ),
    path('logout/', views.logout , name='logout'),
    path('admin_dashboard/', views.admin , name='admin_dashboard'),
    path('customer_page/', views.customerpage , name='customer'),
    path('orderhistory/', views.orderhistory , name='order'),
    path('cart/', views.cart , name='cart'),
    path('add_product/', views.product_add , name='add_product'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

