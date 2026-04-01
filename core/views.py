from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Supplier, Order , Product
from django.contrib.auth import authenticate, login , logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def dashboard(request):
    # 1. Grab everything from the database
    suppliers = Supplier.objects.all()
    products = Product.objects.all()
    orders = Order.objects.all()

    # 2. Package ALL the data your new dashboard.html expects
    context = {
        # The 4 stats you already had
        'total_suppliers': suppliers.count(),
        'total_products': products.count(),
        'total_orders': orders.count(),
        'delivered_orders': orders.filter(status='Delivered').count(),
        
        # The MISSING stats for the Donut Chart
        'pending_orders': orders.filter(status='Pending').count(),
        'shipped_orders': orders.filter(status='Shipped').count(),
        
        # The MISSING data for the tables (grabbing the 5 most recent)
        'recent_orders': orders.order_by('-order_date')[:5], 
        'suppliers': suppliers[:5], 
        
        # The MISSING logic for the Low Stock Alert Banner
        'low_stock_products': products.filter(quantity__lt=10),
        'low_stock_threshold': 10,
    }

    # 3. Send the complete package to the HTML file
    return render(request, 'dashboard.html', context)
    
def home(request):
    return render(request, 'home.html')

@login_required(login_url='/signin/')
def supplier_list(request):
    # 1. Get the suppliers
    suppliers = Supplier.objects.all()
    
    # 2. Get the products so we can trigger the Low Stock Alert on this page
    products = Product.objects.all()

    context = {
        'suppliers': suppliers,
        'low_stock_products': products.filter(quantity__lt=10),
        'low_stock_threshold': 10,
    }
    
    # 3. Render the correct template name
    return render(request, 'supplier_list.html', context)


@login_required(login_url='/signin/')
def order_list(request):
    orders = Order.objects.all()
    
    # Render the correct template name
    return render(request, 'order_list.html', {'orders': orders})
def logout_user(request):
    logout(request) # This destroys the ghost session!
    messages.success(request, 'You have been successfully logged out.')
    return redirect('home')


LOW_STOCK_THRESHOLD = 5


def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Since username and email are the same, we check them directly here
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!') 
            return redirect('dashboard') 
        else:
            messages.error(request, 'Login error: Invalid email or password.')
            return redirect('signin')

    return render(request, 'signin.html')


def signup(request):
    if request.method == 'POST':
        # 1. Capture the data submitted from the HTML form
        name = request.POST.get('name')
        company_name = request.POST.get('company')  # Capturing the company name
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # 2. Check if a user with this email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('signup')

        # 3. Create the user in Django's built-in User model for logging in
        user = User.objects.create_user(
            username=email, 
            email=email, 
            password=password, 
            first_name=name
        )
        
        # 4. Save to YOUR custom Supplier model
        Supplier.objects.create(
            name=company_name, # Mapping the HTML company name to your Supplier 'name' field
            email=email,
            phone="",          # Empty string since it's not in the HTML form yet
            address=""         # Empty string since it's not in the HTML form yet
        )
        
        # 5. Send a success message and redirect to the login page
        messages.success(request, 'Account created! Please sign in.')
        return redirect('signin')

    return render(request, 'signup.html')




def signup(request):
    return render(request, 'signup.html')