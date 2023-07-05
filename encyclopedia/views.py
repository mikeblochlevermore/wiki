from django.shortcuts import render
import markdown2
import random
from urllib.error import HTTPError

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def create(request):
    return render(request, "encyclopedia/create.html", {
    })

def entry(request, title):
    try:
        content = util.get_entry(title)
        if content is None:
            raise HTTPError(None, 404, "Entry not found", None, None)
        # Got help from Chat GPT for the above line
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": markdown2.markdown(content)
        })
    except HTTPError:
        return error(request)

def error(request):
    return render(request, "encyclopedia/error.html")

# The random_page function calls the entry function with a random title from the list of entries
def random_page(request):
    title = random.choice(util.list_entries())
    return entry(request, title)

