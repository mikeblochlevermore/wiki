from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create, name="create"),

    path("edit", views.edit, name="edit"),

    # path that serves all entries
    path("wiki/<str:title>", views.entry, name="entry"),

    # path to a random page
    path("wiki/", views.random_page, name="random"),

    path("error", views.error, name="error"),

    path("search", views.search, name="search"),

    path("git", views.git, name="git"),

    path("git_confirm", views.git_confirm, name="git_confirm")
]
