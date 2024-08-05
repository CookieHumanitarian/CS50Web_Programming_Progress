from django.urls import path

from . import views

app_name = "tasks"
urlpatterns = [
    path("", views.index, name="index"),
    path("random/", views.random_page, name="random"),
    path("wiki", views.search, name="search"),
    path("wiki/<str:name>", views.title, name="title"),
    path("newPage", views.create, name="create"),
    path("edit/<str:name>", views.edit, name="edit")
]
