from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin

from .models import CustomUser, Note, Category
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ("username", "role", "rang", "last_name", "first_name", "surname", "group", "is_active",)
    list_filter = ("role", "rang", "platoon", "group", "unit", "is_active",)
    fieldsets = (
        ("О пользователе", {"fields": ("rang", "last_name", "first_name", "surname", "role", "password")}),
        ("Подразделение", {"fields": ("platoon", "group", "unit")}),
        ("Разрешения и группы", {"fields": ("is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        ('Логин и Пароль', {
            "classes": ("wide",),
            "fields": (
                "username", "password1", "password2", "is_active",
            )}
         ),
        ('О пользователе', {
            "classes": ("wide",),
            "fields": (
                "rang", "last_name", "first_name", "surname", "role",
            )}
         ),
        ('Подразделение', {
            "classes": ("wide",),
            "fields": (
                "platoon", "group", "unit",
            )}
         ),
    )
    ordering = ("group",)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Note)


class CategoryAdmin(DjangoMpttAdmin):
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Category, CategoryAdmin)