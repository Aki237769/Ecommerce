from django.urls import path
from . import views

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
]
