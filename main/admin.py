from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin

from .models import CustomUser, Note, Category
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm

admin.site.site_header = "Панель управления • Workforce Operations"
admin.site.site_title = "Workforce Operations Admin"
admin.site.index_title = "Управление корпоративной структурой и персоналом"


class NoteAdmin(admin.ModelAdmin):
    readonly_fields = ('slug',)
    list_display = ('id', 'type', 'cadet', 'who_gave', 'date', 'check_active')
    list_filter = ('type', 'check_active', 'date')
    search_fields = ('cadet__last_name', 'who_gave__last_name', 'text')


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ("username", "role", "rang", "last_name", "first_name", "surname", "category", "is_active",)
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
admin.site.register(Note, NoteAdmin)
