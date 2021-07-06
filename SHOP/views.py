
##################################################
from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required



#######################################################
#from django.shortcuts import render
from .models import Products
from django.core.paginator import Paginator

from .forms import OrderForm, CreateUserForm





##########################################################






# Create your views here.


def detail(request,id):
    product_objects = Products.objects.get(id=id)
    return render(request,'SHOP/detail.html', {'product_objects': product_objects})

def about(request):
    product_objects = Products.objects.all()
    return render(request,'SHOP/about.html', {'product_objects': product_objects})

#def login(request):
#   product_objects = Products.objects.all()
#   return render(request,'registro/login.html', {'product_objects': product_objects})



############################################################
"""
def registerPage(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        form = CreateUserForm()
        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request,'cuenta creada para' + user)
                return redirect('login')
        context = {'form':form}
        return render(request, 'SHOP/register.html', context)"""

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request,'Ha sido registrado con exito' + user)
                return redirect('login')




        context = {'form':form}
        return render(request, 'SHOP/register.html',context)

############################################################
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request,user)
                return redirect('index')     

            else:
                messages.info(request, 'Usuario o contraseña incorrecta')
                
        context = {}
        return render(request,'SHOP/login.html', context)
"""
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            usernme = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:z
                login(request,user)
                return redirect('index')
            else:
                messages.info(request, 'Username OR password is incorrect')
        
        context = {}
        return render(request,'SHOP/login.html',context)"""
#####################################################################################

def logoutUser(request):
    logout(request)
    return redirect('login')
#####################################################################################
#@login_required(login_url='login')
def index(request):
    product_objects = Products.objects.all()

    #codigo del buscador
    #title__icontains debe tener dos guiones bajos
    item_name = request.GET.get ('item_name') #itm
    if item_name != '' and item_name is not None:
        product_objects = product_objects.filter(title__icontains=item_name)

    #buscador por categoria
    item_category = request.GET.get ('item_category') #itm
    if item_category != '' and item_category is not None:
        product_objects = product_objects.filter(category__icontains=item_category)

    #codigo de paginacion #comentario
    paginator= Paginator(product_objects,10)
    page = request.GET.get('page')
    product_objects = paginator.get_page(page)

    return render(request,'SHOP/index.html', {'product_objects': product_objects})

@login_required(login_url='login')
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()

    total_orders= orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'orders':orders, 'customers':customers,
    'total_orders':total_orders,'delivered':delivered,
    'pending':pending}

    return render(request, 'SHOP/index.html', context)
	

@login_required(login_url='login')
def products(request):
    products = Product.objects.all()
    
    return render(request, 'shop/products.html', {'products':products})


@login_required(login_url='login')
def customer(request, pk_test):
	customer = Customer.objects.get(id=pk_test)

	orders = customer.order_set.all()
	order_count = orders.count()

	myFilter = OrderFilter(request.GET, queryset=orders)
	orders = myFilter.qs 

	context = {'customer':customer, 'orders':orders, 'order_count':order_count,
	'myFilter':myFilter}
	return render(request, 'shop/customer.html',context)


@login_required(login_url='login')
def createOrder(request, pk):
	OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10 )
	customer = Customer.objects.get(id=pk)
	formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
	#form = OrderForm(initial={'customer':customer})
	if request.method == 'POST':
		#print('Printing POST:', request.POST)
		form = OrderForm(request.POST)
		formset = OrderFormSet(request.POST, instance=customer)
		if formset.is_valid():
			formset.save()
			return redirect('/')

	context = {'form':formset}
	return render(request, 'shop/order_form.html', context)

@login_required(login_url='login')
def updateOrder(request, pk):

	order = Order.objects.get(id=pk)
	form = OrderForm(instance=order)

	if request.method == 'POST':
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'shop/order_form.html', context)

@login_required(login_url='login')
def deleteOrder(request, pk):
	order = Order.objects.get(id=pk)
	if request.method == "POST":
		order.delete()
		return redirect('/')

	context = {'item':order}
	return render(request, 'shop/delete.html', context)



