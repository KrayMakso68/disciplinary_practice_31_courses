from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from main.forms import UserLoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.generic import ListView, DetailView

from main.models import Note, CustomUser


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
    template_name = 'main/my_notes.html'

    def get_queryset(self):
        login_user = self.request.user
        notes = Note.objects.filter(cadet=login_user).order_by('-date')
        return notes


class UserNoteView(DetailView):
    model = Note
    context_object_name = 'note'
    template_name = 'main/note_detail.html'


class UnitView(UserPassesTestMixin, ListView):
    def test_func(self):
        return self.request.user.role > CustomUser.LS

    model = CustomUser
    context_object_name = 'cadets_in_unit'
    template_name = 'main/unit.html'

    def get_queryset(self):
        unit = self.kwargs['unit']
        group = self.kwargs['group']
        if self.request.user.role > CustomUser.KO:
            cadets = CustomUser.objects.filter(group=group, unit=unit).order_by('last_name')
        else:
            cadets = CustomUser.objects.filter(group=group, unit=unit).exclude(role=CustomUser.KO).order_by('last_name')
        return cadets


