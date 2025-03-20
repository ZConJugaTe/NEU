# books/admin.py

from django.contrib import admin
from .models import Book, Loan
from .models import PasswordResetRequest

admin.site.register(Book)
admin.site.register(Loan)
admin.site.register(PasswordResetRequest)
