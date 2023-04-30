from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from main.forms import UserLoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.generic import ListView, DetailView

from main.models import Note


@login_required(login_url="login/")
def index(request):
    return render(request, 'main/index.html')


def logoutuser(request):
    logout(request)
    return redirect('login')


class CustomLogin(LoginView):
    authentication_form = UserLoginForm


class UserNotesListView(LoginRequiredMixin, ListView):
    model = Note
    context_object_name = 'user_notes'
    template_name = 'main/mynotes.html'

    def get_queryset(self):
        login_user = self.request.user
        notes = Note.objects.filter(cadet=login_user).order_by('-date')
        return notes


class UserNoteView(DetailView):
    model = Note
    context_object_name = 'note'
    template_name = 'main/note_detail.html'
