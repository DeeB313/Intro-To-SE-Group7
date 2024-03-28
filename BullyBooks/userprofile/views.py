from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from .models import Userprofile
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from inventory.models import Product, Order, OrderItem
from inventory.forms import ProductForm

from django.contrib import messages

# from django.shortcuts import redirect

# Create your views here.
def seller_detail(request, pk):
    user = User.objects.get(pk=pk)
    products = user.products.filter(status=Product.ACTIVE)
    return render(request, 'userprofile/seller_detail.html', {
        'user': user,
        'products': products
    })

def sign_up(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            userprofile = Userprofile.objects.create(user=user)
            return redirect('frontpage')
    else:
        form = UserCreationForm()

    return render(request, 'userprofile/signup.html', {
        'form': form
    })

@login_required
def my_account(request):
    return render(request, 'userprofile/myaccount.html')

@login_required
def my_items(request):
    products = request.user.products.exclude(status=Product.INACTIVE)
    order_list = OrderItem.objects.filter(product__user=request.user)


    return render(request, 'userprofile/myitems.html', {
        'products': products,
        'order_list': order_list
    })

@login_required
def my_items_order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)

    return render(request, 'userprofile/my_items_order_detail.html', {
        'order': order
    })



@login_required
def add_items(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            title = request.POST.get('title')
            product = form.save(commit=False)
            product.user = request.user
            product.slug = slugify(title)
            product.save()

            messages.success(request, 'New item has been added')

            return redirect('my_items')
    else:
        form = ProductForm()
    return render(request, 'userprofile/add-edititems.html', {
        'title': 'Add Items',
        'form': form
    })

@login_required
def edit_items(request, pk):
    product = Product.objects.filter(user=request.user).get(pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            form.save()

            messages.success(request, 'The changes were successful')

            return redirect('my_items')
    else:
        form = ProductForm(instance=product)

    return render(request, 'userprofile/add-edititems.html', {
        'title': 'Edit Items',
        'product': product,
        'form': form,
    })

@login_required
def delete_items(request, pk):
    product = Product.objects.filter(user=request.user).get(pk=pk)
    product.status = Product.INACTIVE
    product.save()

    messages.success(request, 'The product was deleted succesfully')
    return redirect('my_items')
