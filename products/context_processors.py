from .models import Cart


def cart_context(request):
    """Add cart item count to all templates"""
    cart_count = 0
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_count = sum(item.quantity for item in cart.items.all())
        except Cart.DoesNotExist:
            cart_count = 0
    
    return {
        'cart_count': cart_count
    }
