from django.shortcuts import render
from django import forms
import markdown2
import random
from urllib.error import HTTPError
import requests

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


# template for creating and editing entries
class NewEntryForm(forms.Form):
    title = forms.CharField(label="title")
    content = forms.CharField(label="content", widget=forms.Textarea)

class UsernameForm(forms.Form):
    username = forms.CharField(label="username")

def create(request):

    if request.method == "POST":
        # Take in the data the user submitted and save it as form
        form = NewEntryForm(request.POST)

        # Check if form data is valid (server-side)
        if form.is_valid():

            # Isolate the title and content from the 'cleaned' version of form data
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            # Saves only if the new title does not already exist
            if util.get_entry(title) is None:
                util.save_entry(title, content)
            else:
                error_message = "This Entry Already Exists, please choose another title"

                # returns the form with the fields prepopulated with the content that was previously attempted to submit
                return render(request, "encyclopedia/create.html", {
                "form": NewEntryForm(initial={'title': title, 'content': content}),
                'error_message': error_message,
             })

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
        # Credit to Chat GPT for the above line
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

# function to look for partial matches between the query and exisitng titles, part of search function
def partial_matches(query, entries):
    partial_match = []
    for entry in entries:
        # ignores capitalisation in search results
        if query.lower() in entry.lower():
            partial_match.append(entry)
    return partial_match

# For editing pages
def edit(request):
    # will load the editing page with the content from the entry due to be edited
    if request.method == "GET":
        title = request.GET.get('title')
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
                "form": NewEntryForm(initial={'title': title, 'content': content}),
                "title": title,
        })

    if request.method == "POST":
        form = NewEntryForm(request.POST)

        if form.is_valid():

            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            # in edit mode, the entry is simply overwritten, unless the title is altered
            util.save_entry(title, content)
            return entry(request, title)

def git(request):

    if request.method == "GET":
        return render(request, "encyclopedia/git.html", {
            "form": UsernameForm(),
    })

    if request.method == "POST":
        # url to get details of public repositories for that user
        form = UsernameForm(request.POST)

        # Check if form data is valid (server-side)
        if form.is_valid():

            # Get the username inputted
            username = form.cleaned_data["username"]

            repo_url = f"https://api.github.com/users/{username}/repos"
            response = requests.get(repo_url)
            if response.status_code == 200:
                repos = response.json()

            # sorts the json data into a list of names of repositories
            repo_names = []
            for repo in repos:
                repo_names.append(repo["name"])

            # searches for README.md files on the main branch of that username
            for title in repo_names:
                lookup = requests.get(f"https://raw.githubusercontent.com/{username}/{title}/main/README.md")

                # if found, the README files are saved to the wiki
                if lookup.status_code == 200:
                    contents = lookup.text
                    util.save_entry(title, contents)

                # some READMEs are under the blob subfolder, not sure why..
                lookup = requests.get(f"https://raw.githubusercontent.com/{username}/{title}/blob/main/README.md")

                # if found, the README files are saved to the wiki
                if lookup.status_code == 200:
                    contents = lookup.text
                    util.save_entry(title, contents)

        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })
