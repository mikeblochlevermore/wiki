from django.shortcuts import render
import markdown2
import random

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def create(request):
    return render(request, "encyclopedia/create.html", {
    })

def entry(request, title):
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": markdown2.markdown(util.get_entry(title))
    })

def random_page(request):
    title = random.choice(util.list_entries())
    return entry(request, title)

def error(request):
    return render(request, "encyclopedia/error.html", {
    })