from django.urls import path
from . import views
from .views import CustomLogin

urlpatterns = [
    path("", views.index, name='home'),
    path('login/', CustomLogin.as_view(), name="login")
]
