# books/forms.py

from django import forms
from .models import Book, Loan
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# 图书表单
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'published_date', 'isbn']

# 借书表单
class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ['return_date']  # 确保这里只包含 `Loan` 模型中定义的字段
        widgets = {
            'return_date': forms.DateInput(attrs={'type': 'date'}),
        }

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("此邮箱已经被注册！")
        return email