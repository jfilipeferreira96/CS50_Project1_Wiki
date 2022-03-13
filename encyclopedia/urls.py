from django.urls import include, path

from . import views

app_name = 'wiki'

urlpatterns = [
    path("", views.index, name="index"),
    path("new", views.new, name="new"),
    path("random", views.random, name="random"),
    path("search", views.search_entry, name="search"),
    path("wiki/<str:entry_title>", views.title, name="title"),
    path("edit/<str:entry_title>", views.edit, name="edit")
]
