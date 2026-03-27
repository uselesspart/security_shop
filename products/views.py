from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Product, Cart, CartItem


def catalog(request):
    """Display all active products in the catalog"""
    products = Product.objects.filter(is_active=True)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    context = {
        'products': products,
        'search_query': search_query,
    }
    return render(request, 'products/catalog.html', context)


def product_detail(request, product_id):
    """Display detailed information about a specific product"""
    product = get_object_or_404(Product, id=product_id, is_active=True)
    context = {
        'product': product,
    }
    return render(request, 'products/product_detail.html', context)


@login_required
def add_to_cart(request, product_id):
    """Add a product to the user's cart"""
    product = get_object_or_404(Product, id=product_id, is_active=True)
    
    # Get or create cart for the user
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Get or create cart item
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 1}
    )
    
    if not created:
        # If item already exists, increment quantity
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f'Increased quantity of {product.name} in your cart.')
    else:
        messages.success(request, f'Added {product.name} to your cart.')
    
    # Redirect back to the referring page or catalog
    next_url = request.GET.get('next', 'catalog')
    return redirect(next_url)


@login_required
def view_cart(request):
    """Display the user's shopping cart"""
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.select_related('product').all()
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
    }
    return render(request, 'products/cart.html', context)


@login_required
def remove_from_cart(request, item_id):
    """Remove an item from the cart"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    product_name = cart_item.product.name
    cart_item.delete()
    messages.success(request, f'Removed {product_name} from your cart.')
    return redirect('view_cart')


@login_required
def update_cart_quantity(request, item_id):
    """Update the quantity of an item in the cart"""
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, f'Updated quantity for {cart_item.product.name}.')
        else:
            product_name = cart_item.product.name
            cart_item.delete()
            messages.success(request, f'Removed {product_name} from your cart.')
    
    return redirect('view_cart')


@login_required
def clear_cart(request):
    """Clear all items from the user's cart"""
    if request.method == 'POST':
        cart = get_object_or_404(Cart, user=request.user)
        cart.items.all().delete()
        messages.success(request, 'Your cart has been cleared.')
    return redirect('view_cart')
