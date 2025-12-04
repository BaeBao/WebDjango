import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatbot_project.settings')
django.setup()

from shop.models import Category, Brand, Product
from django.contrib.auth.models import User

# Tạo superuser nếu chưa có
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("✓ Đã tạo superuser: admin/admin123")

# Tạo danh mục
categories_data = [
    {'name': 'Điện thoại cao cấp', 'slug': 'dien-thoai-cao-cap', 'description': 'Điện thoại flagship'},
    {'name': 'Điện thoại tầm trung', 'slug': 'dien-thoai-tam-trung', 'description': 'Điện thoại giá tốt'},
    {'name': 'Laptop Gaming', 'slug': 'laptop-gaming', 'description': 'Laptop chơi game'},
    {'name': 'Laptop Văn phòng', 'slug': 'laptop-van-phong', 'description': 'Laptop làm việc'},
]

for cat_data in categories_data:
    Category.objects.get_or_create(slug=cat_data['slug'], defaults=cat_data)
print(f"✓ Đã tạo {len(categories_data)} danh mục")

# Tạo thương hiệu
brands_data = [
    {'name': 'Apple', 'slug': 'apple'},
    {'name': 'Samsung', 'slug': 'samsung'},
    {'name': 'Xiaomi', 'slug': 'xiaomi'},
    {'name': 'OPPO', 'slug': 'oppo'},
    {'name': 'Dell', 'slug': 'dell'},
    {'name': 'HP', 'slug': 'hp'},
    {'name': 'Asus', 'slug': 'asus'},
    {'name': 'Lenovo', 'slug': 'lenovo'},
]

for brand_data in brands_data:
    Brand.objects.get_or_create(slug=brand_data['slug'], defaults=brand_data)
print(f"✓ Đã tạo {len(brands_data)} thương hiệu")

# Tạo sản phẩm điện thoại
phones_data = [
    {
        'name': 'iPhone 15 Pro Max',
        'slug': 'iphone-15-pro-max',
        'category': Category.objects.get(slug='dien-thoai-cao-cap'),
        'brand': Brand.objects.get(slug='apple'),
        'product_type': 'phone',
        'description': 'iPhone 15 Pro Max với chip A17 Pro mạnh mẽ, camera 48MP, màn hình Super Retina XDR 6.7 inch',
        'price': 29990000,
        'discount_price': 27990000,
        'stock': 50,
        'processor': 'Apple A17 Pro',
        'ram': '8GB',
        'storage': '256GB',
        'screen_size': '6.7 inch Super Retina XDR',
        'battery': '4422 mAh',
        'operating_system': 'iOS 17',
        'camera': 'Camera chính 48MP, Ultra Wide 12MP, Telephoto 12MP',
        'sim': '2 SIM (nano-SIM và eSIM)',
        'is_featured': True,
    },
    {
        'name': 'Samsung Galaxy S24 Ultra',
        'slug': 'samsung-galaxy-s24-ultra',
        'category': Category.objects.get(slug='dien-thoai-cao-cap'),
        'brand': Brand.objects.get(slug='samsung'),
        'product_type': 'phone',
        'description': 'Galaxy S24 Ultra với bút S Pen, camera 200MP, màn hình Dynamic AMOLED 2X 6.8 inch',
        'price': 26990000,
        'discount_price': 24990000,
        'stock': 40,
        'processor': 'Snapdragon 8 Gen 3',
        'ram': '12GB',
        'storage': '256GB',
        'screen_size': '6.8 inch Dynamic AMOLED 2X',
        'battery': '5000 mAh',
        'operating_system': 'Android 14',
        'camera': 'Camera chính 200MP, Ultra Wide 12MP, Telephoto 50MP, Telephoto 10MP',
        'sim': '2 SIM (nano-SIM và eSIM)',
        'is_featured': True,
    },
    {
        'name': 'Xiaomi 14 Pro',
        'slug': 'xiaomi-14-pro',
        'category': Category.objects.get(slug='dien-thoai-cao-cap'),
        'brand': Brand.objects.get(slug='xiaomi'),
        'product_type': 'phone',
        'description': 'Xiaomi 14 Pro với camera Leica, chip Snapdragon 8 Gen 3, sạc nhanh 120W',
        'price': 19990000,
        'discount_price': 17990000,
        'stock': 35,
        'processor': 'Snapdragon 8 Gen 3',
        'ram': '12GB',
        'storage': '256GB',
        'screen_size': '6.73 inch AMOLED',
        'battery': '4880 mAh',
        'operating_system': 'Android 14',
        'camera': 'Camera Leica 50MP + 50MP + 50MP',
        'sim': '2 nano-SIM',
        'is_featured': True,
    },
    {
        'name': 'OPPO Find X7',
        'slug': 'oppo-find-x7',
        'category': Category.objects.get(slug='dien-thoai-tam-trung'),
        'brand': Brand.objects.get(slug='oppo'),
        'product_type': 'phone',
        'description': 'OPPO Find X7 với camera Hasselblad, màn hình AMOLED 120Hz',
        'price': 14990000,
        'stock': 30,
        'processor': 'MediaTek Dimensity 9300',
        'ram': '12GB',
        'storage': '256GB',
        'screen_size': '6.78 inch AMOLED',
        'battery': '5000 mAh',
        'operating_system': 'Android 14',
        'camera': 'Camera Hasselblad 50MP + 50MP + 64MP',
        'sim': '2 nano-SIM',
        'is_featured': False,
    },
]

for phone_data in phones_data:
    Product.objects.get_or_create(slug=phone_data['slug'], defaults=phone_data)
print(f"✓ Đã tạo {len(phones_data)} điện thoại")

# Tạo sản phẩm laptop
laptops_data = [
    {
        'name': 'MacBook Pro 16 M3 Max',
        'slug': 'macbook-pro-16-m3-max',
        'category': Category.objects.get(slug='laptop-gaming'),
        'brand': Brand.objects.get(slug='apple'),
        'product_type': 'laptop',
        'description': 'MacBook Pro 16 inch với chip M3 Max, màn hình Liquid Retina XDR, hiệu năng đỉnh cao',
        'price': 89990000,
        'discount_price': 84990000,
        'stock': 20,
        'processor': 'Apple M3 Max 16-core CPU',
        'ram': '36GB Unified Memory',
        'storage': '1TB SSD',
        'screen_size': '16.2 inch Liquid Retina XDR',
        'battery': 'Lên đến 22 giờ',
        'operating_system': 'macOS Sonoma',
        'graphics_card': '40-core GPU',
        'weight': '2.16 kg',
        'is_featured': True,
    },
    {
        'name': 'Dell XPS 15 9530',
        'slug': 'dell-xps-15-9530',
        'category': Category.objects.get(slug='laptop-van-phong'),
        'brand': Brand.objects.get(slug='dell'),
        'product_type': 'laptop',
        'description': 'Dell XPS 15 với màn hình OLED 3.5K, Intel Core i7 thế hệ 13',
        'price': 45990000,
        'discount_price': 42990000,
        'stock': 25,
        'processor': 'Intel Core i7-13700H',
        'ram': '16GB DDR5',
        'storage': '512GB SSD',
        'screen_size': '15.6 inch OLED 3.5K',
        'battery': '86 Wh',
        'operating_system': 'Windows 11 Pro',
        'graphics_card': 'NVIDIA RTX 4050 6GB',
        'weight': '1.86 kg',
        'is_featured': True,
    },
    {
        'name': 'Asus ROG Strix G16',
        'slug': 'asus-rog-strix-g16',
        'category': Category.objects.get(slug='laptop-gaming'),
        'brand': Brand.objects.get(slug='asus'),
        'product_type': 'laptop',
        'description': 'Laptop gaming Asus ROG với RTX 4070, màn hình 240Hz',
        'price': 42990000,
        'discount_price': 39990000,
        'stock': 30,
        'processor': 'Intel Core i9-13980HX',
        'ram': '16GB DDR5',
        'storage': '1TB SSD',
        'screen_size': '16 inch FHD 240Hz',
        'battery': '90 Wh',
        'operating_system': 'Windows 11 Home',
        'graphics_card': 'NVIDIA RTX 4070 8GB',
        'weight': '2.5 kg',
        'is_featured': True,
    },
    {
        'name': 'HP Pavilion 15',
        'slug': 'hp-pavilion-15',
        'category': Category.objects.get(slug='laptop-van-phong'),
        'brand': Brand.objects.get(slug='hp'),
        'product_type': 'laptop',
        'description': 'Laptop văn phòng HP Pavilion với thiết kế mỏng nhẹ',
        'price': 16990000,
        'stock': 40,
        'processor': 'Intel Core i5-1335U',
        'ram': '8GB DDR4',
        'storage': '512GB SSD',
        'screen_size': '15.6 inch FHD',
        'battery': '41 Wh',
        'operating_system': 'Windows 11 Home',
        'graphics_card': 'Intel Iris Xe Graphics',
        'weight': '1.75 kg',
        'is_featured': False,
    },
    {
        'name': 'Lenovo ThinkPad X1 Carbon',
        'slug': 'lenovo-thinkpad-x1-carbon',
        'category': Category.objects.get(slug='laptop-van-phong'),
        'brand': Brand.objects.get(slug='lenovo'),
        'product_type': 'laptop',
        'description': 'ThinkPad X1 Carbon Gen 11 - Laptop doanh nhân cao cấp',
        'price': 38990000,
        'discount_price': 35990000,
        'stock': 15,
        'processor': 'Intel Core i7-1355U',
        'ram': '16GB LPDDR5',
        'storage': '512GB SSD',
        'screen_size': '14 inch WUXGA',
        'battery': '57 Wh',
        'operating_system': 'Windows 11 Pro',
        'graphics_card': 'Intel Iris Xe Graphics',
        'weight': '1.12 kg',
        'is_featured': True,
    },
]

for laptop_data in laptops_data:
    Product.objects.get_or_create(slug=laptop_data['slug'], defaults=laptop_data)
print(f"✓ Đã tạo {len(laptops_data)} laptop")

print("\n✅ Hoàn tất! Dữ liệu mẫu đã được thêm vào database.")
print("\n📝 Thông tin đăng nhập:")
print("   URL: http://127.0.0.1:8000/admin/")
print("   Username: admin")
print("   Password: admin123")
