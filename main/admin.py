from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin

from .models import CustomUser, Note, Category
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm


class Slug_Admin(admin.ModelAdmin):
    readonly_fields = ('slug',)


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ("username", "role", "rang", "last_name", "first_name", "surname", "is_active",)
    list_filter = ("role", "rang", "is_active",)
    fieldsets = (
        ("О пользователе", {"fields": ("rang", "last_name", "first_name", "surname", "role", "category", "password")}),
        ("Уникальный идентификатор", {"fields": ("slug",)}),
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
                "rang", "last_name", "first_name", "surname", "role", "category",
            )}
         ),
    )
    ordering = ()
    readonly_fields = ('slug',)  # отключить, если надо заново создать суперпользователя с нормальным slug


class CategoryAdmin(DjangoMpttAdmin):
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Note, Slug_Admin)
