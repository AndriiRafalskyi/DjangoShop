from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product, Variation
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from constants.variation_category_choices import COLOR_VARIATION, SIZE_VARIATION
import logging
logger = logging.getLogger('django')

def add_product_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)

    variations = []

    if request.POST:
        if COLOR_VARIATION in request.POST:
            variations.append(Variation.objects.get(product=product, variation_category=COLOR_VARIATION, variation_value=request.POST.get(COLOR_VARIATION)))
        if SIZE_VARIATION in request.POST:
            variations.append(Variation.objects.get(product=product, variation_category=SIZE_VARIATION, variation_value=request.POST.get(SIZE_VARIATION)))
    try:
        cart = Cart.objects.get(cart_id=request.session.session_key)
    except Cart.DoesNotExist:
        request.session.create()
        cart = Cart.objects.create(cart_id=request.session.session_key)
        cart.save()

    
    logger.info(variations)

    cart_item = CartItem.get_item_with_same_variations(CartItem.objects.filter(product=product, cart=cart), variations)
    if cart_item:
        cart_item.quantity += 1
    else:
        cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)
        cart_item.variations.set(variations)

    cart_item.save()
        
    return redirect('cart')

def remove_product_from_cart(request, product_id, remove_completely=False):
    cart = Cart.objects.get(cart_id=request.session.session_key)
    product = get_object_or_404(Product, id=product_id)
    
    variations = []

    if request.POST:
        if COLOR_VARIATION in request.POST:
            variations.append(Variation.objects.get(product=product, variation_category=COLOR_VARIATION, variation_value=request.POST.get(COLOR_VARIATION)))
        if SIZE_VARIATION in request.POST:
            variations.append(Variation.objects.get(product=product, variation_category=SIZE_VARIATION, variation_value=request.POST.get(SIZE_VARIATION)))
    
    cart_item = CartItem.get_item_with_same_variations(CartItem.objects.filter(product=product, cart=cart), variations)
    if cart_item.quantity > 1 and not remove_completely:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=request.session.session_key)
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
            quantity += cart_item.quantity
        tax = 2 * total / 100
        final_total = tax + total
    except ObjectDoesNotExist:
        raise Http404

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'final_total': final_total
    }
    return render(request, 'store/cart.html', context)
