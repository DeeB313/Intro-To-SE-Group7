from django.shortcuts import render, get_object_or_404
from .models import Product, Category

from django.db.models import Q

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
