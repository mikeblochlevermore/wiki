from django.shortcuts import render
from django import forms
import markdown2
import random
from urllib.error import HTTPError

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

class NewEntryForm(forms.Form):
    title = forms.CharField(label="title")
    content = forms.CharField(label="content", widget=forms.Textarea)

def create(request):

    if request.method == "POST":
        # Take in the data the user submitted and save it as form
        form = NewEntryForm(request.POST)

        # Check if form data is valid (server-side)
        if form.is_valid():

            # Isolate the task from the 'cleaned' version of form data
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            # Saves only if the new title does not already exist
            if util.get_entry(title) is None:
                util.save_entry(title, content)
            else:
                return render(request, "encyclopedia/error.html")

            # Sends user to newly-created page
            return entry(request, title)

        else:
            return render(request, "encyclopedia/error.html")
    else:
        return render(request, "encyclopedia/create.html", {
            "form": NewEntryForm()
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
