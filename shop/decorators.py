from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def admin_required(view_func):
    """Decorator để kiểm tra user có quyền admin không"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Vui lòng đăng nhập để tiếp tục!')
            return redirect('login')
        
        if not request.user.is_staff:
            messages.error(request, 'Bạn không có quyền truy cập trang này!')
            return redirect('home')
        
        return view_func(request, *args, **kwargs)
    return wrapper
