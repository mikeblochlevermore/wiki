from django.urls import path
import random
from . import util

from . import views

# calculation to choose a random page

random_page = random.choice(util.list_entries())
# random_page = "git"

urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create, name="create"),

    # path that serves all entries
    path("wiki/<str:title>", views.entry, name="entry"),

    # path to a random page
    path(f"wiki/{random_page}", views.entry, name="random")
]
