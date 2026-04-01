from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('suppliers/', views.supplier_list, name='supplier_list'),
    path('orders/', views.order_list, name='order_list'),
 
    path('dashboard/', views.dashboard, name='dashboard'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_user, name='logout'),
]

 
 
   
