from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q, Avg, Count
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Product, Category, Brand, Cart, CartItem, Order, OrderItem, Review
from .forms import ProductForm, CategoryForm, BrandForm, OrderStatusForm
from .decorators import admin_required
import random
import string

def home(request):
    # Admin tự động chuyển đến dashboard
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_dashboard')
    
    featured_products = Product.objects.filter(is_featured=True, is_available=True)[:8]
    phones = Product.objects.filter(product_type='phone', is_available=True)[:4]
    laptops = Product.objects.filter(product_type='laptop', is_available=True)[:4]
    categories = Category.objects.all()
    brands = Brand.objects.all()
    
    context = {
        'featured_products': featured_products,
        'phones': phones,
        'laptops': laptops,
        'categories': categories,
        'brands': brands,
    }
    return render(request, 'shop/home.html', context)

def product_list(request):
    products = Product.objects.filter(is_available=True)
    
    # Lọc theo loại sản phẩm
    product_type = request.GET.get('type')
    if product_type:
        products = products.filter(product_type=product_type)
    
    # Lọc theo danh mục
    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category__slug=category_slug)
    
    # Lọc theo thương hiệu
    brand_slug = request.GET.get('brand')
    if brand_slug:
        products = products.filter(brand__slug=brand_slug)
    
    # Lọc theo giá
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    
    # Tìm kiếm
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(brand__name__icontains=search_query)
        )
    
    # Sắp xếp
    sort_by = request.GET.get('sort', '-created_at')
    products = products.order_by(sort_by)
    
    # Phân trang
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    products_page = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    brands = Brand.objects.all()
    
    context = {
        'products': products_page,
        'categories': categories,
        'brands': brands,
        'current_type': product_type,
        'current_category': category_slug,
        'current_brand': brand_slug,
    }
    return render(request, 'shop/product_list.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_available=True)
    reviews = product.reviews.all()
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    related_products = Product.objects.filter(
        category=product.category,
        is_available=True
    ).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'related_products': related_products,
    }
    return render(request, 'shop/product_detail.html', context)

def register(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('admin_dashboard')
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        full_name = request.POST.get('full_name', '')
        
        # Validation
        if password != password2:
            messages.error(request, 'Mật khẩu không khớp!')
            return redirect('register')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Tên đăng nhập đã tồn tại!')
            return redirect('register')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email đã được sử dụng!')
            return redirect('register')
        
        # Create user
        user = User.objects.create_user(username=username, email=email, password=password)
        if full_name:
            names = full_name.split(' ', 1)
            user.first_name = names[0]
            if len(names) > 1:
                user.last_name = names[1]
            user.save()
        
        login(request, user)
        messages.success(request, f'Chào mừng {username}! Đăng ký thành công.')
        return redirect('home')
    
    return render(request, 'shop/register.html')

def user_login(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('admin_dashboard')
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Chào mừng trở lại, {user.username}!')
            
            # Kiểm tra next_url
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            
            # Admin vào dashboard, user thường vào home
            if user.is_staff:
                return redirect('admin_dashboard')
            return redirect('home')
        else:
            messages.error(request, 'Tên đăng nhập hoặc mật khẩu không đúng!')
    
    return render(request, 'shop/login.html')

def user_logout(request):
    logout(request)
    messages.success(request, 'Đã đăng xuất thành công!')
    return redirect('home')

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, f'Đã thêm {product.name} vào giỏ hàng!')
    
    # Nếu là AJAX request, trả về JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': f'Đã thêm {product.name} vào giỏ hàng!',
            'cart_count': cart.get_item_count()
        })
    
    return redirect('cart')

@login_required
def buy_now(request, product_id):
    """Thêm sản phẩm vào giỏ hàng và chuyển ngay đến trang giỏ hàng"""
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, f'Đã thêm {product.name} vào giỏ hàng!')
    return redirect('cart')

@login_required
def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    context = {'cart': cart}
    return render(request, 'shop/cart.html', context)

@login_required
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'increase':
            cart_item.quantity += 1
            cart_item.save()
        elif action == 'decrease':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
        elif action == 'remove':
            cart_item.delete()
            messages.success(request, 'Đã xóa sản phẩm khỏi giỏ hàng!')
    
    return redirect('cart')

@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    
    if not cart.items.exists():
        messages.warning(request, 'Giỏ hàng của bạn đang trống!')
        return redirect('cart')
    
    if request.method == 'POST':
        # Tạo đơn hàng
        order_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        
        order = Order.objects.create(
            user=request.user,
            order_number=order_number,
            full_name=request.POST.get('full_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            district=request.POST.get('district'),
            note=request.POST.get('note', ''),
            payment_method=request.POST.get('payment_method'),
            subtotal=cart.get_total(),
            total=cart.get_total() + 30000,
        )
        
        # Tạo order items
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.get_final_price()
            )
            # Giảm số lượng tồn kho
            item.product.stock -= item.quantity
            item.product.save()
        
        # Xóa giỏ hàng
        cart.items.all().delete()
        
        messages.success(request, f'Đặt hàng thành công! Mã đơn hàng: {order_number}')
        return redirect('order_detail', order_id=order.id)
    
    context = {'cart': cart}
    return render(request, 'shop/checkout.html', context)

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    context = {'orders': orders}
    return render(request, 'shop/order_list.html', context)

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    context = {'order': order}
    return render(request, 'shop/order_detail.html', context)

@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        Review.objects.update_or_create(
            product=product,
            user=request.user,
            defaults={'rating': rating, 'comment': comment}
        )
        
        messages.success(request, 'Cảm ơn bạn đã đánh giá!')
        return redirect('product_detail', slug=product.slug)
    
    return redirect('product_detail', slug=product.slug)


# ==================== ADMIN VIEWS ====================

@admin_required
def admin_dashboard(request):
    """Trang dashboard admin"""
    # Thống kê
    total_products = Product.objects.filter(is_available=True).count()
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='pending').count()
    total_users = User.objects.count()
    # Tính tổng doanh thu (tất cả đơn trừ đơn đã hủy)
    total_revenue = sum(order.total for order in Order.objects.exclude(status='cancelled'))
    
    # Đơn hàng gần đây
    recent_orders = Order.objects.all().order_by('-created_at')[:10]
    
    # Sản phẩm sắp hết hàng
    low_stock_products = Product.objects.filter(stock__lte=10, is_available=True).order_by('stock')[:10]
    
    # Thống kê theo tháng
    today = timezone.now()
    this_month_orders = Order.objects.filter(created_at__month=today.month, created_at__year=today.year).count()
    # Tính doanh thu tháng này (tất cả đơn trừ đơn đã hủy)
    this_month_revenue = sum(
        order.total for order in Order.objects.filter(
            created_at__month=today.month, 
            created_at__year=today.year
        ).exclude(status='cancelled')
    )
    
    context = {
        'total_products': total_products,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'total_users': total_users,
        'total_revenue': total_revenue,
        'recent_orders': recent_orders,
        'low_stock_products': low_stock_products,
        'this_month_orders': this_month_orders,
        'this_month_revenue': this_month_revenue,
    }
    return render(request, 'shop/admin/dashboard.html', context)

@admin_required
def admin_products(request):
    """Danh sách sản phẩm"""
    products = Product.objects.all().order_by('-created_at')
    
    # Tìm kiếm
    search = request.GET.get('search')
    if search:
        products = products.filter(
            Q(name__icontains=search) | 
            Q(brand__name__icontains=search)
        )
    
    # Lọc theo loại
    product_type = request.GET.get('type')
    if product_type:
        products = products.filter(product_type=product_type)
    
    # Phân trang
    paginator = Paginator(products, 20)
    page = request.GET.get('page')
    products = paginator.get_page(page)
    
    context = {'products': products}
    return render(request, 'shop/admin/products.html', context)

@admin_required
def admin_product_add(request):
    """Thêm sản phẩm mới"""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Đã thêm sản phẩm "{product.name}" thành công!')
            return redirect('admin_products')
    else:
        form = ProductForm()
    
    context = {'form': form, 'action': 'add'}
    return render(request, 'shop/admin/product_form.html', context)

@admin_required
def admin_product_edit(request, product_id):
    """Sửa sản phẩm"""
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Đã cập nhật sản phẩm "{product.name}" thành công!')
            return redirect('admin_products')
    else:
        form = ProductForm(instance=product)
    
    context = {'form': form, 'product': product, 'action': 'edit'}
    return render(request, 'shop/admin/product_form.html', context)

@admin_required
def admin_product_delete(request, product_id):
    """Xóa sản phẩm"""
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f'Đã xóa sản phẩm "{product_name}" thành công!')
        return redirect('admin_products')
    
    context = {'product': product}
    return render(request, 'shop/admin/product_delete.html', context)

@admin_required
def admin_orders(request):
    """Danh sách đơn hàng"""
    orders = Order.objects.all().order_by('-created_at')
    
    # Lọc theo trạng thái
    status = request.GET.get('status')
    if status:
        orders = orders.filter(status=status)
    
    # Tìm kiếm
    search = request.GET.get('search')
    if search:
        orders = orders.filter(
            Q(order_number__icontains=search) |
            Q(full_name__icontains=search) |
            Q(phone__icontains=search)
        )
    
    # Phân trang
    paginator = Paginator(orders, 20)
    page = request.GET.get('page')
    orders = paginator.get_page(page)
    
    context = {'orders': orders}
    return render(request, 'shop/admin/orders.html', context)

@admin_required
def admin_order_detail(request, order_id):
    """Chi tiết đơn hàng"""
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        form = OrderStatusForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, f'Đã cập nhật trạng thái đơn hàng #{order.order_number}!')
            return redirect('admin_order_detail', order_id=order.id)
    else:
        form = OrderStatusForm(instance=order)
    
    context = {'order': order, 'form': form}
    return render(request, 'shop/admin/order_detail.html', context)

@admin_required
def admin_categories(request):
    """Danh sách danh mục"""
    categories = Category.objects.all().order_by('name')
    context = {'categories': categories}
    return render(request, 'shop/admin/categories.html', context)

@admin_required
def admin_category_add(request):
    """Thêm danh mục"""
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'Đã thêm danh mục "{category.name}" thành công!')
            return redirect('admin_categories')
    else:
        form = CategoryForm()
    
    context = {'form': form, 'action': 'add'}
    return render(request, 'shop/admin/category_form.html', context)

@admin_required
def admin_category_edit(request, category_id):
    """Sửa danh mục"""
    category = get_object_or_404(Category, id=category_id)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'Đã cập nhật danh mục "{category.name}" thành công!')
            return redirect('admin_categories')
    else:
        form = CategoryForm(instance=category)
    
    context = {'form': form, 'category': category, 'action': 'edit'}
    return render(request, 'shop/admin/category_form.html', context)

@admin_required
def admin_category_delete(request, category_id):
    """Xóa danh mục"""
    category = get_object_or_404(Category, id=category_id)
    
    if request.method == 'POST':
        category_name = category.name
        category.delete()
        messages.success(request, f'Đã xóa danh mục "{category_name}" thành công!')
        return redirect('admin_categories')
    
    context = {'category': category}
    return render(request, 'shop/admin/category_delete.html', context)

@admin_required
def admin_brands(request):
    """Danh sách thương hiệu"""
    brands = Brand.objects.all().order_by('name')
    context = {'brands': brands}
    return render(request, 'shop/admin/brands.html', context)

@admin_required
def admin_brand_add(request):
    """Thêm thương hiệu"""
    if request.method == 'POST':
        form = BrandForm(request.POST, request.FILES)
        if form.is_valid():
            brand = form.save()
            messages.success(request, f'Đã thêm thương hiệu "{brand.name}" thành công!')
            return redirect('admin_brands')
    else:
        form = BrandForm()
    
    context = {'form': form, 'action': 'add'}
    return render(request, 'shop/admin/brand_form.html', context)

@admin_required
def admin_brand_edit(request, brand_id):
    """Sửa thương hiệu"""
    brand = get_object_or_404(Brand, id=brand_id)
    
    if request.method == 'POST':
        form = BrandForm(request.POST, request.FILES, instance=brand)
        if form.is_valid():
            brand = form.save()
            messages.success(request, f'Đã cập nhật thương hiệu "{brand.name}" thành công!')
            return redirect('admin_brands')
    else:
        form = BrandForm(instance=brand)
    
    context = {'form': form, 'brand': brand, 'action': 'edit'}
    return render(request, 'shop/admin/brand_form.html', context)

@admin_required
def admin_brand_delete(request, brand_id):
    """Xóa thương hiệu"""
    brand = get_object_or_404(Brand, id=brand_id)
    
    if request.method == 'POST':
        brand_name = brand.name
        brand.delete()
        messages.success(request, f'Đã xóa thương hiệu "{brand_name}" thành công!')
        return redirect('admin_brands')
    
    context = {'brand': brand}
    return render(request, 'shop/admin/brand_delete.html', context)

@admin_required
def admin_users(request):
    """Danh sách người dùng"""
    users = User.objects.all().order_by('-date_joined')
    
    # Tìm kiếm
    search = request.GET.get('search')
    if search:
        users = users.filter(
            Q(username__icontains=search) |
            Q(email__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search)
        )
    
    # Phân trang
    paginator = Paginator(users, 20)
    page = request.GET.get('page')
    users = paginator.get_page(page)
    
    context = {'users': users}
    return render(request, 'shop/admin/users.html', context)
