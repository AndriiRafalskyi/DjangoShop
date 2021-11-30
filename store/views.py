from django.shortcuts import render, get_object_or_404
from .models import Product, Category

# Create your views here.
def store(request, category_slug=None):
    if category_slug:
        category = get_object_or_404(Category, category_slug=category_slug)
        products = Product.objects.all().filter(category=category, is_available=True)
    else:
        products = Product.objects.all().filter(is_available=True)
    
    context = {
        'products': products
    }

    return render(request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):
    try:
        product = Product.objects.get(category__category_slug=category_slug, slug=product_slug)
    except Exception as e:
        raise e

    context = {
        'product': product
    }

    return render(request, 'store/product_detail.html', context)
