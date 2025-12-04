# TechShop - Website Thương Mại Điện Tử

🛒 Website bán điện thoại và laptop được xây dựng bằng Django

## ✨ Tính năng

### Khách hàng:
- 🏠 Trang chủ với sản phẩm nổi bật
- 📱 Danh sách sản phẩm (điện thoại, laptop)
- 🔍 Tìm kiếm và lọc sản phẩm
- 🛒 Giỏ hàng với giao diện đẹp
- 💳 Đặt hàng và thanh toán
- 📋 Quản lý đơn hàng cá nhân
- ⭐ Đánh giá sản phẩm
- 🔐 Đăng ký/Đăng nhập

### Admin:
- 📊 Dashboard thống kê
- 📦 Quản lý sản phẩm (CRUD)
- 🛍️ Quản lý đơn hàng
- 🏷️ Quản lý danh mục & thương hiệu
- 👥 Quản lý người dùng
- 📸 Upload hình ảnh sản phẩm

## 🚀 Công nghệ sử dụng

- **Backend:** Django 5.2.7
- **Database:** SQLite
- **Frontend:** HTML, CSS (Inline)
- **Python:** 3.13

## 📦 Cài đặt

### 1. Clone repository
```bash
git clone https://github.com/BaeBao/webdjango.git
cd webdjango
```

### 2. Tạo virtual environment
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac
```

### 3. Cài đặt dependencies
```bash
pip install django pillow
```

### 4. Tạo file .env
```
SECRET_KEY=your-secret-key-here
DEBUG=True
```

### 5. Chạy migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Tạo superuser (admin)
```bash
python manage.py createsuperuser
```

### 7. Chạy server
```bash
python manage.py runserver
```

Truy cập: http://127.0.0.1:8000

## 👤 Tài khoản mặc định

Nếu đã chạy `add_sample_data.py`:
- **Username:** admin
- **Password:** admin123

## 📁 Cấu trúc thư mục

```
webdjango/
├── chatbot_project/      # Cấu hình Django chính
├── shop/                 # App chính
│   ├── templates/        # HTML templates
│   ├── models.py         # Database models
│   ├── views.py          # Logic xử lý
│   ├── urls.py           # URL routing
│   └── forms.py          # Forms
├── media/                # Hình ảnh upload
├── manage.py             # Django management
└── requirements.txt      # Dependencies
```

## 🎨 Giao diện

- Thiết kế hiện đại với gradient màu tím
- Responsive layout
- Card sản phẩm với hover effects
- Badge giảm giá
- Icon SVG cho giỏ hàng
- Animation mượt mà

## 📝 License

MIT License

## 👨‍💻 Tác giả

BaeBao

## 🤝 Đóng góp

Mọi đóng góp đều được chào đón! Hãy tạo pull request.
