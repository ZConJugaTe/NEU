# books/models.py

from django.db import models

# 图书模型定义
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    published_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)

    def __str__(self):
        return self.title

    def is_borrowed(self):
        # 检查是否有未归还的借阅记录
        return self.loans.filter(returned=False).exists()

from django.contrib.auth.models import User

#借阅记录模型定义
class Loan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loans', default=1)  # 借阅用户
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='loans')  # 借阅书籍
    loan_date = models.DateField(auto_now_add=True)  # 借阅日期
    return_date = models.DateField(null=True, blank=True)  # 归还日期（可为空）
    returned = models.BooleanField(default=False)  # 是否归还

    def __str__(self):
        return f"{self.user.username} 借阅了 {self.book.title}"


# 修改密码信息模型定义
class PasswordResetRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_reset_requests')  # 用户信息
    request_date = models.DateField(auto_now_add=True)  # 提出日期
    is_resolved = models.BooleanField(default=False)  # 是否解决

    def __str__(self):
        return f"密码重置请求 - 用户: {self.user.username}, 提出日期: {self.request_date}"