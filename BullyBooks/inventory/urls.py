from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search, name='search'),
    path('compareitems/<slug:category_slug>/<int:product_id>/', views.compare, name='compare'),
    path('add-to-cart/<int:product_id>', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<str:product_id>', views.remove_from_cart, name='remove_from_cart'),
    path('change-quantity/<str:product_id>', views.change_quantity, name='change_quantity'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/checkout/', views.checkout, name='checkout'),
    path('cart/success/', views.success, name='success'),
    path('<slug:slug>/', views.category_detail, name='category_detail'),
    path('<slug:category_slug>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('admin_unlist_item/<str:product_id>/<path:from_path>/', views.admin_unlist_item, name="admin_unlist_item")
]