# books/views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Loan
from .forms import BookForm, LoanForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages  # 用于显示消息
from django.contrib.auth import login  # 导入 login 函数
from django.db.models import Q
import datetime
from django.db import connection
from collections import defaultdict
from django.utils.timezone import now
import json
from .forms import CustomUserCreationForm  # 引入自定义表单
import csv
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # 保存用户
            login(request, user)  # 自动登录
            messages.success(request, f"欢迎，{user.username}！注册成功！")
            print(connection.queries)  # 打印所有的 SQL 查询
            return redirect('book_list')  # 跳转到书籍列表页面
        else:
            messages.error(request, "注册失败，请检查输入内容！")
    else:
        form = CustomUserCreationForm()
    return render(request, 'books/register.html', {'form': form})

def custom_logout(request):
    logout(request)
    return redirect('login')  # 登出后跳转到登录页面

from django.db import connection
from django.shortcuts import render
from .models import Book

@login_required
def book_list(request):
    # 获取查询参数
    title_query = request.GET.get('title', '')
    author_query = request.GET.get('author', '')
    published_date_query = request.GET.get('published_date', '')
    isbn_query = request.GET.get('isbn', '')

    # 基础 SQL 查询
    sql_query = """
        SELECT b.id, b.title, b.author, b.published_date, b.isbn,
               COALESCE(MAX(CASE WHEN l.returned = FALSE THEN 1 ELSE 0 END), 0) AS is_borrowed
        FROM books_book b
        LEFT JOIN books_loan l ON b.id = l.book_id
        WHERE 1=1
    """

    # 动态添加条件
    params = []
    if title_query:
        sql_query += " AND b.title LIKE %s"
        params.append('%' + title_query + '%')
    if author_query:
        sql_query += " AND b.author LIKE %s"
        params.append('%' + author_query + '%')
    if published_date_query:
        sql_query += " AND b.published_date LIKE %s"
        params.append('%' + published_date_query + '%')
    if isbn_query:
        sql_query += " AND b.isbn LIKE %s"
        params.append('%' + isbn_query + '%')

    # 分组和排序
    sql_query += " GROUP BY b.id ORDER BY b.id"

    # 执行查询
    with connection.cursor() as cursor:
        cursor.execute(sql_query, params)
        books = cursor.fetchall()

    # 转换查询结果为字典列表
    book_list = [
        {
            'id': book[0],
            'title': book[1],
            'author': book[2],
            'published_date': book[3],
            'isbn': book[4],
            'is_borrowed': book[5] == 1,  # 0: 未借出, 1: 已借出
        }
        for book in books
    ]

    # 计算搜索到的书籍数量
    book_count = len(book_list)

    book_borrowed_count = 0
    for book in books:
        if book[5]==1:
            book_borrowed_count += 1

    return render(request, 'books/book_list.html', {
        'books': book_list,
        'title': title_query,
        'author': author_query,
        'published_date': published_date_query,
        'isbn': isbn_query,
        'book_count':book_count,
        'book_borrowed_count':book_borrowed_count,
        'book_save_count':book_count-book_borrowed_count
    })

@login_required
def book_batch_create(request):
    if request.method == 'POST' and request.FILES['csv_file']:
        csv_file = request.FILES['csv_file']
        fs = FileSystemStorage()
        filename = fs.save(csv_file.name, csv_file)
        file_path = fs.url(filename)

        try:
            with open(file_path[1:], mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # 跳过表头

                # 使用原生 SQL 批量插入
                sql_query = """
                    INSERT INTO books_book (title, author, published_date, isbn)
                    VALUES (%s, %s, %s, %s)
                """
                params = []
                
                # 收集要插入的数据
                for row in reader:
                    title, author, published_date, isbn = row
                    params.append((title.strip(), author.strip(), published_date.strip(), isbn.strip()))
                
                # 使用批量插入
                with connection.cursor() as cursor:
                    cursor.executemany(sql_query, params)

            messages.success(request, "书籍批量导入成功！")
            return redirect('book_list')
        except Exception as e:
            messages.error(request, f"导入失败：{e}")
            return redirect('book_list')

    return render(request, 'books/book_batch_upload.html')

@login_required
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'books/book_detail.html', {'book': book})

@login_required
def book_create(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        author = request.POST.get('author', '').strip()
        published_date = request.POST.get('published_date', '').strip()
        isbn = request.POST.get('isbn', '').strip()

        # 检查输入内容是否完整
        if not (title and author and published_date and isbn):
            messages.error(request, "所有字段都是必填项！")
            return redirect('book_create')

        try:
            # 执行 SQL 插入语句
            sql_query = """
                INSERT INTO books_book (title, author, published_date, isbn)
                VALUES (%s, %s, %s, %s)
            """
            with connection.cursor() as cursor:
                cursor.execute(sql_query, [title, author, published_date, isbn])

            messages.success(request, "书籍添加成功！")
            return redirect('book_list')
        except Exception as e:
            messages.error(request, f"添加书籍时发生错误：{str(e)}")
            return redirect('book_create')
    else:
        # 渲染表单页面
        return render(request, 'books/book_form.html')

@login_required
def book_edit(request, pk):
    if not request.user.is_staff:  # 或者使用 request.user.is_superuser
        messages.error(request, "您没有权限编辑书籍。")
        return redirect('book_list')

    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        # 从表单中获取新值
        title = request.POST.get('title', '').strip()
        author = request.POST.get('author', '').strip()
        published_date = request.POST.get('published_date', '').strip()
        isbn = request.POST.get('isbn', '').strip()

        # 检查输入内容是否完整
        if not (title and author and published_date and isbn):
            messages.error(request, "所有字段都是必填项！")
            return redirect('book_edit', pk=pk)

        try:
            # 执行 SQL 更新语句
            sql_query = """
                UPDATE books_book
                SET title = %s, author = %s, published_date = %s, isbn = %s
                WHERE id = %s
            """
            with connection.cursor() as cursor:
                cursor.execute(sql_query, [title, author, published_date, isbn, pk])

            messages.success(request, "书籍编辑成功！")
            return redirect('book_list')

        except Exception as e:
            messages.error(request, f"编辑书籍时发生错误：{str(e)}")
            return redirect('book_edit', pk=pk)

    else:
        # 渲染表单页面
        return render(request, 'books/book_form.html', {'book': book})


@login_required
def loan_create(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    # 检查书籍是否已被借出
    if book.is_borrowed():
        messages.error(request, "该书已被借出！")
        return redirect('book_list')

    if request.user.loans.filter(returned=False).exists():
        messages.error(request, "您已经借过书了！")
        return redirect('book_list')

    if request.method == 'POST':
        form = LoanForm(request.POST)
        if form.is_valid():
            loan = form.save(commit=False)
            loan.book = book
            loan.user = request.user
            loan.save()
            messages.success(request, "借书成功！")
            return redirect('book_list')
    else:
        form = LoanForm()
    return render(request, 'books/loan_form.html', {'form': form, 'book': book})

# 删除书籍视图
@login_required
def book_delete(request, pk):
    if not request.user.is_staff:  # 或者使用 request.user.is_superuser
        messages.error(request, "您没有权限删除书籍。")
        return redirect('book_list')
    
    book = get_object_or_404(Book, pk=pk)

    # 检查书籍是否正在被借阅
    if book.is_borrowed():
        messages.error(request, "该书籍正在被借阅，无法删除。")
        return redirect('book_list')

    if request.method == 'POST':
        book.delete()
        messages.success(request, "书籍删除成功！")
        return redirect('book_list')
    return render(request, 'books/book_confirm_delete.html', {'book': book})

# 借阅书籍的视图
@login_required
def loaned_books(request):
    # 获取查询参数
    title_query = request.GET.get('title', '').strip()
    author_query = request.GET.get('author', '').strip()
    loan_date_query = request.GET.get('loan_date', '').strip()
    return_date_query = request.GET.get('return_date', '').strip()

    # 获取当前年份
    current_year = datetime.date.today().year

    # 判断是否为管理员，管理员查看所有用户的借阅记录
    if request.user.is_staff:  # 如果是管理员
        user_id_condition = ""  # 管理员不限制用户
        params = []
    else:  # 普通用户只能查看自己的借阅记录
        user_id_condition = "AND l.user_id = %s"
        params = [request.user.id]

    # 基础 SQL 查询
    sql_query = """
        SELECT l.id, b.title, b.author, l.loan_date, l.returned, l.return_date, u.email
        FROM books_loan l
        JOIN books_book b ON l.book_id = b.id
        JOIN auth_user u ON l.user_id = u.id
        WHERE 1=1
    """

    # 动态添加条件
    if title_query:
        sql_query += " AND b.title LIKE %s"
        params.append('%' + title_query + '%')
    if author_query:
        sql_query += " AND b.author LIKE %s"
        params.append('%' + author_query + '%')
    if loan_date_query:
        sql_query += " AND l.loan_date = %s"
        params.append(loan_date_query)
    if return_date_query:
        sql_query += " AND l.return_date = %s"
        params.append(return_date_query)
    
    # 如果不是管理员，添加用户ID条件
    sql_query += user_id_condition

    # 排序
    sql_query += " ORDER BY l.loan_date DESC"

    # 执行查询
    with connection.cursor() as cursor:
        cursor.execute(sql_query, params)
        loans = cursor.fetchall()

    # 转换查询结果为字典列表
    loan_list = [
        {
            'id': loan[0],
            'title': loan[1],
            'author': loan[2],
            'loan_date': loan[3],
            'returned': loan[4],
            'return_date': loan[5] if loan[4] else None,  # 如果已归还，返回日期
            'user_email': loan[6]  # 显示借阅用户的邮箱
        }
        for loan in loans
    ]

    # 获取每个月的借书数量
    monthly_loans_query = """
        SELECT strftime('%%m', l.loan_date) AS month, COUNT(*) AS count
        FROM books_loan l
        WHERE strftime('%%Y', l.loan_date) = %s
    """

    # 如果是管理员，查询所有用户的借书数量；否则只查询当前用户的借书数量
    if not request.user.is_staff:
        monthly_loans_query += " AND l.user_id = %s"
        monthly_loans_params = [str(current_year), request.user.id]
    else:
        monthly_loans_params = [str(current_year)]

    monthly_data = defaultdict(int)
    with connection.cursor() as cursor:
        cursor.execute(monthly_loans_query, monthly_loans_params)
        for month, count in cursor.fetchall():
            # 判断month是否为None或其他无效值
            if month is not None:
                try:
                    # 如果month有效，将其转换为整数
                    month_int = int(month)
                    if 1 <= month_int <= 12:  # 确保是有效的月份
                        monthly_data[month_int] = count
                except ValueError:
                    # 如果month不是有效的数字，跳过该条记录
                    continue

    # 转换为每月的数据列表（保证 1 到 12 月都有数据）
    monthly_loans = [monthly_data.get(month, 0) for month in range(1, 13)]

    return render(request, 'books/loaned_books.html', {
        'loans': loan_list,
        'title_query': title_query,
        'author_query': author_query,
        'loan_date_query': loan_date_query,
        'monthly_loans': json.dumps(monthly_loans),  # 序列化为 JSON 格式字符串
    })


@login_required
def return_book(request, loan_id):
    # 如果是管理员，跳过用户检查，直接查找借阅记录
    if request.user.is_staff:
        loan = get_object_or_404(Loan, id=loan_id)
    else:
        loan = get_object_or_404(Loan, id=loan_id, user=request.user)

    # 如果是管理员，直接强制标记为已归还
    if request.user.is_staff or not loan.returned:
        loan.returned = True
        loan.return_date = now()  # 自动填充当前日期为归还日期
        loan.save()
        if request.user.is_staff:
            messages.success(request, "管理员强制还书成功！")
        else:
            messages.success(request, "还书成功！")
    else:
        messages.error(request, "该书已被归还！")

    return redirect('loaned_books')  # 还书后重定向到已借书籍列表

# 查看用户信息
@login_required
def view_users(request):
    # 判断是否为管理员
    if not request.user.is_staff:
        # 普通用户只能查看自己的信息
        user_id = request.user.id
        sql_query = """SELECT u.id, u.username, u.email, u.password 
                       FROM auth_user u
                       WHERE u.id = %s"""  # 只显示当前用户的信息
        params = [user_id]
    else:
        # 管理员查看所有非超级管理员的用户
        username_query = request.GET.get('username', '').strip()
        email_query = request.GET.get('email', '').strip()

        # 构建 SQL 查询条件
        sql_query = """SELECT u.id, u.username, u.email, u.password 
                       FROM auth_user u
                       WHERE u.is_staff = 0"""  # 排除超级管理员
        
        params = []
        if username_query:
            sql_query += " AND username LIKE %s"
            params.append(f"%{username_query}%")
        
        if email_query:
            sql_query += " AND email LIKE %s"
            params.append(f"%{email_query}%")
        
        # 分组和排序
        sql_query += " ORDER BY u.id"

    # 执行原生 SQL 查询
    with connection.cursor() as cursor:
        cursor.execute(sql_query, params)
        users = cursor.fetchall()  # 获取查询结果

    # 返回结果
    return render(request, 'books/view_users.html', {
        'users': users,  # 直接传递 users
    })


from django.contrib.auth.hashers import make_password, check_password  # 导入密码加密工具
from django.contrib.auth import update_session_auth_hash
#修改密码视图
@login_required
def change_password(request, user_id=None):
    # 判断是否为管理员或者是修改自己密码的情况
    if not request.user.is_staff and request.user.id != user_id:
        messages.error(request, "没有权限修改密码")
        return redirect('book_list')

    # 确定目标用户：如果是管理员，则修改指定用户的密码，否则修改当前登录用户的密码
    if request.user.is_staff:
        # 如果是管理员，允许修改指定用户的密码
        user = User.objects.get(id=user_id)
    else:
        # 如果是普通用户，只能修改自己的密码
        user = request.user

    # 处理密码修改
    if request.method == 'POST':
        # 如果是普通用户，必须输入原密码
        if not request.user.is_staff:
            old_password = request.POST.get('old_password', '').strip()
            if not check_password(old_password, user.password):
                messages.error(request, "原密码不正确")
                return redirect('change_password', user_id=user.id)

        new_password = request.POST.get('new_password', '').strip()
        confirm_new_password = request.POST.get('confirm_new_password', '').strip()

        # 验证新密码和确认密码是否一致
        if new_password != confirm_new_password:
            messages.error(request, "新密码和确认密码不一致")
        # 新密码不能为空并且满足长度要求
        elif not new_password:
            messages.error(request, "请输入有效的新密码")
        else:
            # 使用 Django 的 make_password 函数对密码进行加密
            encrypted_password = make_password(new_password)

            # 更新用户密码
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE auth_user SET password = %s WHERE id = %s",
                    [encrypted_password, user.id]
                )

            # 密码修改成功后，刷新 session 以保持用户登录状态
            update_session_auth_hash(request, user)

            messages.success(request, f"用户 {user.username} 的密码已成功修改")
            return redirect('view_users' if request.user.is_staff else 'book_list')  # 密码修改后跳回用户列表或首页

    # 渲染修改密码页面
    return render(request, 'books/change_password.html', {
        'user': user
    })

from .models import PasswordResetRequest
# 忘记密码视图
def forget_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # 获取用户名
        email = request.POST.get('email')  # 获取邮箱
        try:
            user = User.objects.get(username=username, email=email)  # 根据用户名和邮箱查找用户
            # 创建密码重置请求记录
            PasswordResetRequest.objects.create(user=user)
            messages.success(request, "密码重置请求已提交，我们将尽快处理。")
            return redirect('login')  # 重定向到登录页面
        except User.DoesNotExist:
            messages.error(request, "用户名或邮箱不匹配，请检查后再试。")
            return redirect('forget_password')  # 如果用户名和邮箱不匹配，重定向回忘记密码页面
    
    return render(request, 'books/forget_password.html')

# 用户请求视图
@login_required
def user_requests(request):
    # 获取当前用户
    user = request.user

    # 获取查询条件（如果有的话）
    username_query = request.GET.get('username', '')
    request_date_query = request.GET.get('request_date', '')
    is_resolved_query = request.GET.get('is_resolved', '')

    # 构造基本 SQL 查询
    sql_query = """
        SELECT pr.id, pr.user_id, pr.request_date, pr.is_resolved, u.username
        FROM books_passwordresetrequest pr
        JOIN auth_user u ON pr.user_id = u.id
        WHERE 1=1
    """

    # 构造动态条件
    params = []
    if username_query:
        sql_query += " AND u.username LIKE %s"
        params.append(f'%{username_query}%')
    
    if request_date_query:
        sql_query += " AND pr.request_date = %s"
        params.append(request_date_query)
    
    if is_resolved_query:
        sql_query += " AND pr.is_resolved = %s"
        params.append('1' if is_resolved_query == 'True' else '0')

    # 如果是管理员，显示所有请求，否则只显示当前用户的请求
    if not user.is_staff:
        sql_query += " AND pr.user_id = %s"
        params.append(user.id)

    sql_query += " ORDER BY pr.request_date DESC"  # 按请求日期降序排序

    # 执行 SQL 查询
    with connection.cursor() as cursor:
        cursor.execute(sql_query, params)
        result = cursor.fetchall()
    
    # 处理查询结果
    requests = []
    for row in result:
        requests.append({
            'id': row[0],
            'user_id': row[1],
            'request_date': row[2],
            'is_resolved': row[3],
            'username': row[4],  # 获取用户名
        })

    return render(request, 'books/user_request.html', {
        'requests': requests,
        'username_query': username_query,
        'request_date_query': request_date_query,
        'is_resolved_query': is_resolved_query,
    })

# 标记请求为已解决
@login_required
def resolve_password_request(request, request_id):
    try:
        # 获取对应的密码重置请求
        reset_request = PasswordResetRequest.objects.get(id=request_id)
        # 更新为已解决
        reset_request.is_resolved = True
        reset_request.save()

        messages.success(request, '密码重置请求已标记为已解决。')
    except PasswordResetRequest.DoesNotExist:
        messages.error(request, '该密码重置请求不存在。')

    return redirect('user_requests')  # 重定向回用户请求页面