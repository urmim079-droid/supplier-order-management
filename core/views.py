from django.shortcuts import render
from .models import Supplier, Order

def home(request):
    return render(request, 'home.html')

def supplier_list(request):
    suppliers = Supplier.objects.all()
    return render(request, 'supplier_list.html', {'suppliers': suppliers})

def order_list(request):
    orders = Order.objects.all()
    return render(request, 'order_list.html', {'orders': orders})

