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

# Function for searching the wiki
def search(request):
    # get the entry from the search field
    query = request.GET.get('q')

    # check whether the entry is an exact match to a title
    content = util.get_entry(query)

    if content is None:

        partial_match = partial_matches(query, util.list_entries())

        return render(request, "encyclopedia/search.html", {
            "query": query,
            "partial_match": partial_match,
        })
    else:
        title = query
        return entry(request, title)

# function to look for partial matches between the query and exisitng titles
def partial_matches(query, entries):
    partial_match = []
    for entry in entries:
        # ignores capitalisation in search results
        if query.lower() in entry.lower():
            partial_match.append(entry)
    return partial_match
