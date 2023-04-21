from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from main.forms import UserLoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


@login_required(login_url="login/")
def index(request):
    return render(request, 'main/index.html')


def logoutuser(request):
    logout(request)
    return redirect('login')


class CustomLogin(LoginView):
    authentication_form = UserLoginForm
