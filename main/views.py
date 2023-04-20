from django.contrib.auth.views import LoginView
from django.shortcuts import render
from main.forms import UserLoginForm


def index(request):
    return render(request, 'main/index.html')


class CustomLogin(LoginView):
    authentication_form = UserLoginForm
