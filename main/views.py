import json
import matplotlib.pyplot as plt
import seaborn as sns

from docxtpl import DocxTemplate, InlineImage

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse, FileResponse
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
        promotions = 0  # поощрения
        punishments = 0  # взыскания
        withdrawals = 0  # снятие взяскания
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


def statistica_docxcreate(request):
    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
    if is_ajax:
        data = json.loads(request.POST.get('pars_data'))
        doc = DocxTemplate('main/static/main/docx/Statistica_template.docx')
        plt_data = []
        plt_labels = []
        if data['promotions']:
            plt_data.append(data['promotions'])
            plt_labels.append('Поощрения')
        if data['punishments']:
            plt_data.append(data['punishments'])
            plt_labels.append('Взыскания')
        if data['withdrawals']:
            plt_data.append(data['withdrawals'])
            plt_labels.append('Снятия взыскания')
        colors = sns.color_palette('pastel')[0:3]
        plt.switch_backend('agg')
        plt.pie(plt_data, labels=plt_labels, colors=colors, autopct='%.0f%%', wedgeprops=dict(width=0.6))
        plt.savefig('main/static/main/docx/pie.png')
        plt.close()

        context = {
            'userNode': request.user.category,
            'dateInterval': request.POST.get('dateInterval'),
            'all_notes': data['all_notes'],
            'promotions': data['promotions'],
            'punishments': data['punishments'],
            'withdrawals': data['withdrawals'],
            'pieImg': InlineImage(doc, 'main/static/main/docx/pie.png')
        }
        doc.render(context)
        doc.save('main/static/main/docx/Statistica.docx')

        file_location = 'main/static/main/docx/Statistica.docx'

        with open(file_location, 'rb') as worddoc:  # read as binary
            content = worddoc.read()  # Read the file
            response = HttpResponse(
                content,
                content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            )
            response['Content-Disposition'] = 'attachment; filename=Statistica.docx'
            response['Content-Length'] = len(content)  # calculate length of content
            return response
    return JsonResponse({})
