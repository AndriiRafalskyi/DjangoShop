from .models import Cart, CartItem

def counter(request):
    cart_count = 0
    if 'admin' in request.path:
        return {}
    try:
        cart = Cart.objects.get(cart_id=request.session.session_key)
        cart_items = CartItem.objects.filter(cart=cart)
        for cart_item in cart_items:
            cart_count += cart_item.quantity
    except Cart.DoesNotExist:
        pass
    finally:
        return dict(cart_count=cart_count)
            

