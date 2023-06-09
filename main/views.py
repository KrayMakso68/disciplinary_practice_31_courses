import json
from io import StringIO

from docxtpl import DocxTemplate

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from main.forms import UserLoginForm, NoteCreateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.generic import ListView, DetailView, CreateView
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
    template_name = 'main/user_notes.html'

    def get_queryset(self):
        slug = self.kwargs["slug"]
        user = CustomUser.objects.filter(slug=slug).first()
        notes = user.notes.all()
        return notes

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs["slug"]
        user = CustomUser.objects.filter(slug=slug).first()
        context["user"] = user
        return context


class UserNoteView(DetailView):
    model = Note
    context_object_name = 'note'
    template_name = 'main/note_detail.html'


class GroupsContentView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    def test_func(self):
        return self.request.user.role > CustomUser.LS

    model = CustomUser
    context_object_name = 'cadets'
    template_name = 'main/content_groups.html'

    def get_queryset(self):
        login_user = self.request.user
        main_node = self.request.user.category
        if main_node.is_leaf_node():
            cadets = main_node.staff.exclude(slug=login_user.slug)
        else:
            cadets = CustomUser.objects.none()
            nodes = main_node.get_descendants()
            for node in nodes:
                cadets = cadets | node.staff.all()
        return cadets.order_by('last_name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["main_node"] = self.request.user.category
        return context


class NoteCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    def test_func(self):
        return self.request.user.role > CustomUser.LS

    model = Note
    form_class = NoteCreateForm
    context_object_name = 'note'
    template_name = 'main/note_create.html'

    def get_success_url(self):
        return reverse('view_user_notes', kwargs={"slug": self.kwargs["slug"]})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs["slug"]
        user = CustomUser.objects.get(slug=slug)
        context["for_user"] = user
        return context

    def post(self, *args, **kwargs):
        form = NoteCreateForm(self.request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.cadet = CustomUser.objects.get(slug=self.kwargs["slug"])
            instance.who_gave = self.request.user
            instance.save()
            return HttpResponseRedirect(self.get_success_url())
        return render(self.request, 'main/note_create.html', {'form': form})


def statistica_view(request):
    return render(request, 'main/statistica.html')


def statistica_search(request):
    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
    if is_ajax:
        startdate = request.POST.get('startdate')
        enddate = request.POST.get('enddate')
        promotions = 0       #поощрения
        punishments = 0      #взыскания
        withdrawals = 0      #снятие взяскания
        user_node = request.user.category
        all_lower_nodes = user_node.get_descendants(include_self=True)
        for node in all_lower_nodes:
            cadets = node.staff.all()
            for cadet in cadets:
                notes = cadet.notes.all().filter(date__range=[startdate, enddate])
                for note in notes:
                    if note.type == 'Поощрение':
                        promotions = promotions + 1
                    elif note.type == 'Взыскание':
                        punishments = punishments + 1
                    else:
                        withdrawals = withdrawals + 1
        all_notes = promotions + punishments + withdrawals
        return JsonResponse({'promotions': promotions,
                             'punishments': punishments,
                             'withdrawals': withdrawals,
                             'all_notes': all_notes
                             })
    return JsonResponse({})


def statistica_download(request):
    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
    if is_ajax:
        data = json.loads(request.POST.get('pars_data'))
        doc = DocxTemplate('main/static/main/docx/Statistica_template.docx')
        context = {
            'userNode': request.user.category,
            'dateInterval': request.POST.get('dateInterval'),
            'all_notes': data['all_notes'],
            'promotions': data['promotions'],
            'punishments': data['punishments'],
            'withdrawals': data['withdrawals'],
            'pieImg': '',
        }
        doc.render(context)
        doc.save('main/static/main/docx/Statistica.docx')
        #тута нужна выгрузка файла пользователю на скачивание!!!

        return JsonResponse({})
    return JsonResponse({})
