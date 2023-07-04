from django.shortcuts import render
import markdown2

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
        "content": markdown2.markdown(util.get_entry(title))
    })

