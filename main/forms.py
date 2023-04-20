from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, UsernameField
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = "__all__"


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = "__all__"

# https://testdriven.io/blog/django-custom-user-model/


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(required=True, widget=forms.TextInput(
        attrs={
            'type': 'text',
            'class': 'form-control',
            'placeholder': 'Логин',
            'id': 'floatingInput'
        }
    ))
    password = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={
            'type': 'password',
            'class': 'form-control',
            'placeholder': 'Пароль',
            'id': 'floatingPassword',
        }
    ))
    error_messages = {
        "invalid_login": "Ah, ah, ah. You didn't say the magic word!",
        "inactive": "Permission denied",
    }

# https://stackoverflow.com/questions/55369645/how-to-customize-default-auth-login-form-in-django
# https://pytutorial.com/loginview-django-example/