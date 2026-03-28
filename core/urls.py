from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('suppliers/', views.supplier_list),
    path('orders/', views.order_list),
]
 
