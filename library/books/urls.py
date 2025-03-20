# books/urls.py

from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView,LoginView
from .views import custom_logout, register


urlpatterns = [
    path('login/', LoginView.as_view(template_name='books/login.html'), name='login'),  # 登录页面
    path('logout/', custom_logout, name='logout'),    # 登出页面
    path('register/', register, name='register'),
    path('', views.book_list, name='book_list'),
    path('book/new/', views.book_create, name='book_create'),
    path('books/batch_create/', views.book_batch_create, name='book_batch_create'),
    path('book/edit/<int:pk>/', views.book_edit, name='book_edit'),
    path('book/<int:book_id>/loan/', views.loan_create, name='loan_create'),
    path('book/<int:pk>/delete/', views.book_delete, name='book_delete'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'), 
    path('loaned_books/', views.loaned_books, name='loaned_books'),  # 已借书籍列表
    path('return_book/<int:loan_id>/', views.return_book, name='return_book'),  # 还书
    path('users/', views.view_users, name='view_users'),  # 管理员查看所有用户信息
    path('users/<int:user_id>/change_password/', views.change_password, name='change_password'),
    path('forget-password/', views.forget_password, name='forget_password'),
    path('user-requests/', views.user_requests, name='user_requests'),  # 显示用户请求列表
    path('user-request/resolve/<int:request_id>/', views.resolve_password_request, name='resolve_password_request'),  # 标记为已解决
]
