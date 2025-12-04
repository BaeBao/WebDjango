from django import forms
from .models import Product, Category, Brand, Order

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 'slug', 'category', 'brand', 'product_type',
            'description', 'price', 'discount_price', 'stock', 'image',
            'processor', 'ram', 'storage', 'screen_size', 'battery',
            'operating_system', 'camera', 'sim', 'graphics_card', 'weight',
            'is_featured', 'is_available'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tên sản phẩm'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'slug-san-pham'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'brand': forms.Select(attrs={'class': 'form-control'}),
            'product_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Mô tả sản phẩm'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'discount_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'processor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'VD: Intel Core i7'}),
            'ram': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'VD: 16GB'}),
            'storage': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'VD: 512GB SSD'}),
            'screen_size': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'VD: 15.6 inch'}),
            'battery': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'VD: 5000 mAh'}),
            'operating_system': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'VD: Windows 11'}),
            'camera': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'VD: 48MP'}),
            'sim': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'VD: 2 SIM'}),
            'graphics_card': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'VD: RTX 4060'}),
            'weight': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'VD: 2.5 kg'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name', 'slug', 'logo']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'logo': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }

class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
