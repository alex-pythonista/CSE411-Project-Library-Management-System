from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from .filters import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth.models import Group
from datetime import datetime
from django.db.models import Q
# yesterday = datetime.date.today() - datetime.timedelta(days=1)

@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    context = {'form': form}

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='students')
            user.groups.add(group)
            Customer.objects.create(user=user)
            messages.success(request, "Account was created for " + username)
            return redirect('login')

    return render(request, 'accounts/register.html', context)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or password is incorrect!')
    context = {}
    return render(request, 'accounts/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    allIssuedBooksToday = orders.filter(date_created__gte=datetime.today().date())
    total_customers = customers.count()
    late_submissions = orders.filter(status='Late Submission', date_created__gte=datetime.today().date()).count()
    returned = orders.filter(status='Returned', date_created__gte=datetime.today().date()).count()
    issued = orders.filter(status='Issued', date_created__gte=datetime.today().date()).count()
    if request.method == 'GET':
        search = request.GET.get('search', '')
        result = Customer.objects.filter(name__icontains=search)

    context = {'orders': orders, 'customers': customers, 'total_customers': total_customers, 'returned': returned, 'issued': issued, 'late_submissions': late_submissions, 'allIssuedBooksToday': allIssuedBooksToday, 'search': search, 'result': result}

    return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='login')
def products(request):
    products = Product.objects.all()
    if request.method == 'GET':
        search = request.GET.get('search', '')
        result = Product.objects.filter(name__icontains=search)
    return render(request, 'accounts/products.html', {'products': products, 'search': search, 'result': result})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admins'])
def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)

    orders = customer.order_set.all()
    order_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {'customer': customer, 'orders': orders, 'order_count': order_count, 'filter': myFilter}
    return render(request, 'accounts/customer.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admins'])
def createOrder(request):
    form = OrderForm()
    if request.method == 'POST':
        # print("Printing POST:", request.POST)
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admins'])
def updateOrder(request, pk):
    order = Order.objects.get(pk=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        # print("Printing POST:", request.POST)
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admins'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context = {'item': order}
    return render(request, 'accounts/delete.html', context)

# def aboutPage(request):
#     return render(request, 'accounts/about.html', {})

def contactPage(request):
    return render(request, 'accounts/contactus.html', {})

@login_required(login_url='login')
@allowed_users(allowed_roles=['students'])
def userPage(request):
    orders = request.user.customer.order_set.all()

    context = {'orders': orders,}

    return render(request, 'accounts/user.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admins'])
def issuedBooks(request):
    issued = Order.objects.filter(status='Issued')
    context = {'issued': issued}
    return render(request, 'accounts/issuedBooks.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admins'])
def lateSubmissions(request):
    late_submissions = Order.objects.filter(status='Late Submission')
    context = {'late_submissions': late_submissions}
    return render(request, 'accounts/lateSubmissions.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admins'])
def returnedBooks(request):
    returnedBooks = Order.objects.filter(Q(status="Returned") | Q(status="Late Submission"))
    context = {'returned': returnedBooks}
    return render(request, 'accounts/returnedBooks.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['students'])
def accountSettings(request):
	customer = request.user.customer
	form = CustomerForm(instance=customer)

	if request.method == 'POST':
		form = CustomerForm(request.POST, request.FILES,instance=customer)
		if form.is_valid():
			form.save()


	context = {'form':form}
	return render(request, 'accounts/account_settings.html', context)