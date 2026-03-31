from django.shortcuts import render
from .models import Supplier, Product, Order
from django.db.models import Q

LOW_STOCK_THRESHOLD = 5


def home(request):
    return render(request, 'home.html')


def supplier_list(request):
    suppliers = Supplier.objects.all()
    low_stock_products = Product.objects.filter(
        quantity__lte=LOW_STOCK_THRESHOLD
    ).order_by('quantity')

    return render(request, 'supplier_list.html', {
        'suppliers': suppliers,
        'low_stock_products': low_stock_products,
        'low_stock_threshold': LOW_STOCK_THRESHOLD,
    })


def order_list(request):
    orders = Order.objects.select_related(
        'supplier', 'product'
    ).order_by('-order_date')

    return render(request, 'order_list.html', {
        'orders': orders
    })


def dashboard(request):
    total_suppliers = Supplier.objects.count()
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    delivered_orders = Order.objects.filter(status='Delivered').count()

    return render(request, 'dashboard.html', {
        'total_suppliers': total_suppliers,
        'total_products': total_products,
        'total_orders': total_orders,
        'delivered_orders': delivered_orders,
    })
def signin(request):
    return render(request, 'signin.html')

def signup(request):
    return render(request, 'signup.html')