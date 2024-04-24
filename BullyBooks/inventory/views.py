#import json
#import stripe

#from django.http import JsonResponse
from django.http import HttpRequest
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, OrderItem
from .cart import Cart
from .forms import OrderForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


from django.db.models import Q

def compare(request, category_slug, product_id):
    # Get the original product
    original_product = get_object_or_404(Product, pk=product_id)

    # Get the category of the original product
    category = original_product.category

    # Get similar products in the same category
    similar_products = category.products.filter(status=Product.ACTIVE).exclude(pk=original_product.pk)[:2]

    return render(request, 'inventory/compare.html', {
        'category': category,
        'original_product': original_product,
        'similar_products': similar_products,
    }) 

def search(request):
    results = request.GET.get('results', '')
    products = Product.objects.filter(status=Product.ACTIVE).filter(Q(title__icontains=results) | Q(description__icontains=results))

    return render(request, 'inventory/search.html', {
        'results': results,
        'products': products,
    })

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.filter(status=Product.ACTIVE)
    return render(request, 'inventory/category_detail.html', {
        'category': category,
        'products': products,
    })

def product_detail(request, category_slug, slug):
    product = get_object_or_404(Product, slug=slug, status=Product.ACTIVE)
    return render(request, 'inventory/product_detail.html', {
        'product': product
    })

def view_cart(request):
    cart = Cart(request)

    return render(request, 'inventory/view_cart.html', {
        'cart': cart
    })

@login_required
def checkout(request):
    cart = Cart(request)

    if cart.cart_cost() == 0:
        return redirect('view_cart')

    if request.method == "POST":
        form = OrderForm(request.POST)

        if form.is_valid():
            total_price = 0
            #items = []

            #for item in cart:
            #    product = item['product']
            #    total_price += product.price * int(item['quantity'])
#
#                items.append({
#                    'price_data': {
#                        'currency': 'usd',
#                        'product_data': {
#                            'name': product.title,
#                        },
#                        'unit_amount': product.price,
#                    },
#                    'quantity': item['quantity']
#                })
#
#           stripe.api_key = settings.STRIPE_SECRET_KEY
#            session = stripe.checkout.Session.create(
#                payment_method_types=['card'],
#                line_items=items,
#                mode='payment',
#                success_url='http://127.0.0.1:8000/cart/success/',
#                cancel_url='http://127.0.0.1:8000/cart/'
#            )
#            payment_intent = session.payment_intent


            order = form.save(commit=False)
            order.created_by = request.user
            order.payment = True
#            order.payment_intent = payment_intent
            order.total_paid = total_price
            order.save()

            for item in cart:
                product = item['product']
                quantity = int(item['quantity'])
                price = product.price * quantity

                item = OrderItem.objects.create(order=order, product=product, price=price, quantity=quantity)

            cart.clear()


            return redirect('success')
    else:
        form = OrderForm()

    messages.success(request, 'The order has been placed successfully')
    return render(request, 'inventory/checkout.html', {
        'cart': cart,
        'form': form,
#        'pub_key': settings.STRIPE_PUBLIC_KEY,
    })



def add_to_cart(request, product_id):
    cart = Cart(request)
    cart.add(product_id)

    return redirect('view_cart')

def remove_from_cart(request, product_id):
    cart = Cart(request)
    cart.remove(str(product_id))

    return redirect('view_cart')

def change_quantity(request, product_id):
    action = request.GET.get('action', '')

    if action:
        quantity = 1

        if action == 'decrease':   
            quantity = -1

        cart = Cart(request)
        cart.add(product_id, quantity, True)

    return redirect('view_cart')

def success(request):
    return render(request, 'inventory/success.html')

def admin_unlist_item(request, product_id, from_path):
    product = Product.objects.filter(id=product_id)[0]
    product.delete()

    return redirect(from_path)