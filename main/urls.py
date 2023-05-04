from django.urls import path
from . import views
from .views import CustomLogin, UserNotesListView, UserNoteView

urlpatterns = [
    path('', views.index, name='home'),
    path('login/', CustomLogin.as_view(), name="login"),
    path('logout/', views.logoutuser, name="logout"),
    path('my_notes/', UserNotesListView.as_view(), name='view_my_notes'),
    path('my_notes/<slug:slug>/', UserNoteView.as_view(), name='user_note_detail'),
]
