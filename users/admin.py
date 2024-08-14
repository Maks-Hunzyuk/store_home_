from django.contrib import admin

from users.models import User
from carts.admin import CartTabAmin


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Отображение пользователей в админке"""
    list_display = ("username", "first_name", "last_name", "email",)
    search_fields = ("username", "first_name", "last_name", "email")
    inlines = [CartTabAmin,]

