from django.urls import path
from . import views

urlpatterns = [
    path('catalog/', views.catalog, name='catalog'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),
    path('moderator/products/', views.moderator_product_list, name='moderator_product_list'),
    path('moderator/products/add/', views.moderator_product_create, name='moderator_product_create'),
    path('moderator/products/<int:product_id>/edit/', views.moderator_product_edit, name='moderator_product_edit'),
    path('moderator/products/<int:product_id>/delete/', views.moderator_product_delete, name='moderator_product_delete'),
]
