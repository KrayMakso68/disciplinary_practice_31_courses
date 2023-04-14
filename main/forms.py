from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            'username', 'password', 'is_active', 'role', 'first_name', 'last_name',
            'rang', 'platoon', 'group', 'unit'
        )


# class CustomUserChangeForm(UserChangeForm):
#
#     class Meta:
#         model = CustomUser
#         fields = ("email",)

# https://testdriven.io/blog/django-custom-user-model/