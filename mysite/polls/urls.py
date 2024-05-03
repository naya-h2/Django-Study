from django.urls import path

from . import views #view를 불러온다.

urlpatterns = [
    path("", views.index, name="index"),
]