from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product, Variation
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from constants.variation_category_choices import COLOR_VARIATION, SIZE_VARIATION

def add_product_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)

    color_variation = Variation.objects.get(product=product, variation_category=COLOR_VARIATION, variation_value=request.POST.get(COLOR_VARIATION))
    size_variation = Variation.objects.get(product=product, variation_category=SIZE_VARIATION, variation_value=request.POST.get(SIZE_VARIATION))

    try:
        cart = Cart.objects.get(cart_id=request.session.session_key)
    except Cart.DoesNotExist:
        request.session.create()
        cart = Cart.objects.create(cart_id=request.session.session_key)
        cart.save()
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        
        cart_item.quantity += 1
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)
    finally:
        cart_item.save()

    return redirect('cart')

def remove_product_from_cart(request, product_id, remove_completely=False):
    cart = Cart.objects.get(cart_id=request.session.session_key)
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
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
