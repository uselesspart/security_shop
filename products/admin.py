from django.contrib import admin
from .models import Product, Cart, CartItem


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    list_editable = ('is_active',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Product Information', {
            'fields': ('name', 'price', 'description', 'image', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'get_items_count', 'get_total')
    readonly_fields = ('created_at', 'updated_at')
    
    def get_items_count(self, obj):
        return obj.items.count()
    get_items_count.short_description = 'Items Count'


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'get_subtotal', 'added_at')
    list_filter = ('added_at',)
    readonly_fields = ('added_at',)
