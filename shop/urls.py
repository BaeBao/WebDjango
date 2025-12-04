from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    
    # Auth
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # Cart & Orders
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('buy-now/<int:product_id>/', views.buy_now, name='buy_now'),
    path('update-cart/<int:item_id>/', views.update_cart, name='update_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.order_list, name='order_list'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    
    # Review
    path('review/<int:product_id>/', views.add_review, name='add_review'),
    
    # Admin Panel
    path('my-admin/', views.admin_dashboard, name='admin_dashboard'),
    path('my-admin/products/', views.admin_products, name='admin_products'),
    path('my-admin/products/add/', views.admin_product_add, name='admin_product_add'),
    path('my-admin/products/<int:product_id>/edit/', views.admin_product_edit, name='admin_product_edit'),
    path('my-admin/products/<int:product_id>/delete/', views.admin_product_delete, name='admin_product_delete'),
    path('my-admin/orders/', views.admin_orders, name='admin_orders'),
    path('my-admin/orders/<int:order_id>/', views.admin_order_detail, name='admin_order_detail'),
    path('my-admin/categories/', views.admin_categories, name='admin_categories'),
    path('my-admin/categories/add/', views.admin_category_add, name='admin_category_add'),
    path('my-admin/categories/<int:category_id>/edit/', views.admin_category_edit, name='admin_category_edit'),
    path('my-admin/categories/<int:category_id>/delete/', views.admin_category_delete, name='admin_category_delete'),
    path('my-admin/brands/', views.admin_brands, name='admin_brands'),
    path('my-admin/brands/add/', views.admin_brand_add, name='admin_brand_add'),
    path('my-admin/brands/<int:brand_id>/edit/', views.admin_brand_edit, name='admin_brand_edit'),
    path('my-admin/brands/<int:brand_id>/delete/', views.admin_brand_delete, name='admin_brand_delete'),
    path('my-admin/users/', views.admin_users, name='admin_users'),
]
