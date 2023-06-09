from django.urls import path
from . import views
from .views import CustomLogin, UserNotesListView, UserNoteView, GroupsContentView, NoteCreateView

urlpatterns = [
    path('', views.index, name='home'),
    path('login/', CustomLogin.as_view(), name="login"),
    path('logout/', views.logoutuser, name="logout"),
    path('notes/<slug:slug>/', UserNotesListView.as_view(), name='view_user_notes'),
    path('note/<slug:slug>/', UserNoteView.as_view(), name='user_note_detail'),
    path('group_content/', GroupsContentView.as_view(), name='view_group_content'),
    path('create_note-<slug:slug>/', NoteCreateView.as_view(), name='create_note'),
    path('statistica/', views.statistica_view, name='statistica'),
    path('statistica_search/', views.statistica_search, name='statistica_search'),
    path('statistica_docxcreate/', views.statistica_docxcreate, name='statistica_docxcreate')
]
