from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from cart.models import CartItem
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q

# Create your views here.
def store(request, category_slug=None):
    if category_slug:
        category = get_object_or_404(Category, category_slug=category_slug)
        products = Product.objects.all().filter(category=category, is_available=True).order_by('id')
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')

    products = Paginator(products, 6).get_page(request.GET.get('page'))

    context = {
        'products': products
    }

    return render(request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):
    try:
        product = Product.objects.get(category__category_slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(product=product, cart__cart_id=request.session.session_key).exists()
    except Exception as e:
        raise e

    context = {
        'product': product,
        'in_cart': in_cart
    }

    return render(request, 'store/product_detail.html', context)

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
    context = {
        'products': products
    }
    return render(request, 'store/store.html', context)
