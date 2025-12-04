from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    logo = models.ImageField(upload_to='brands/', blank=True, null=True)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    PRODUCT_TYPE_CHOICES = [
        ('phone', 'Điện thoại'),
        ('laptop', 'Laptop'),
    ]
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')
    product_type = models.CharField(max_length=10, choices=PRODUCT_TYPE_CHOICES)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=0)
    discount_price = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    stock = models.IntegerField(default=0)
    image = models.ImageField(upload_to='products/')
    
    # Thông số kỹ thuật chung
    processor = models.CharField(max_length=200, blank=True)
    ram = models.CharField(max_length=50, blank=True)
    storage = models.CharField(max_length=50, blank=True)
    screen_size = models.CharField(max_length=50, blank=True)
    battery = models.CharField(max_length=100, blank=True)
    operating_system = models.CharField(max_length=100, blank=True)
    
    # Thông số riêng cho điện thoại
    camera = models.CharField(max_length=200, blank=True)
    sim = models.CharField(max_length=100, blank=True)
    
    # Thông số riêng cho laptop
    graphics_card = models.CharField(max_length=200, blank=True)
    weight = models.CharField(max_length=50, blank=True)
    
    is_featured = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def get_final_price(self):
        if self.discount_price:
            return self.discount_price
        return self.price
    
    def get_discount_percentage(self):
        if self.discount_price:
            return int(((self.price - self.discount_price) / self.price) * 100)
        return 0

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/gallery/')
    alt_text = models.CharField(max_length=200, blank=True)
    
    def __str__(self):
        return f"{self.product.name} - Image"

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ('product', 'user')
    
    def __str__(self):
        return f"{self.user.username} - {self.product.name}"

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Cart - {self.user.username}"
    
    def get_total(self):
        return sum(item.get_subtotal() for item in self.items.all())
    
    def get_item_count(self):
        return sum(item.quantity for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('cart', 'product')
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
    def get_subtotal(self):
        return self.product.get_final_price() * self.quantity

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Chờ xác nhận'),
        ('confirmed', 'Đã xác nhận'),
        ('shipping', 'Đang giao hàng'),
        ('delivered', 'Đã giao hàng'),
        ('cancelled', 'Đã hủy'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('cod', 'Thanh toán khi nhận hàng'),
        ('bank', 'Chuyển khoản ngân hàng'),
        ('momo', 'Ví MoMo'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_number = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    note = models.TextField(blank=True)
    
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    subtotal = models.DecimalField(max_digits=10, decimal_places=0)
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=0, default=30000)
    total = models.DecimalField(max_digits=10, decimal_places=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Order {self.order_number}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
    def get_subtotal(self):
        return self.price * self.quantity
