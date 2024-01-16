from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from . import util
import markdown2
from markdown2 import Markdown
import random

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def create(request):

    if request.method == "POST":

        title = request.POST.get("title")
        content = request.POST.get("content")

        if title and content:
            if util.get_entry(title):
                return render(request, "encyclopedia/error.html", {
                    "error": f"Entry already exists sorry."
                })
            
            util.save_entry(title, content)
            return render(request, "encyclopedia/created.html", {
                "entry_title": title    
            })
        
        else:

            return render(request, "encyclopedia/error.html", {
                "error": f"One or both fields are empty please try again"
            })
                
    else:

        return render(request, "encyclopedia/create.html")

def random_page(request):
    
    if request.method == "POST":
    
        entries = util.list_entries()

        entry = random.choice(entries)

        return render(request, "encyclopedia/entry.html", {
            "entry_title": entry,
            "entry": util.get_entry(entry),
            "entry_markdown2": markdown2.markdown(util.get_entry(entry))
        })
    
    else:
        return render(request, "encyclopedia/random.html")
    
def entry(request):

    if request.method == "POST":

        
        entry = request.POST.get("entry")

        if util.get_entry(entry):

            return render(request, "encyclopedia/entry.html", {
                "entry_title": entry,
                "entry": util.get_entry(entry),
                "entry_markdown2": markdown2.markdown(util.get_entry(entry))
            })
        else:
            entries = util.list_entries()
            matching_titles = []

            for title in entries:
                if entry in title:
                    matching_titles.append(title)
            
            if not matching_titles:
                return render(request, "encyclopedia/error.html", {
                    "error": f"No entries here :("
                })
            else:
                print(matching_titles)
                return render(request, "encyclopedia/suggestions.html", {
                    "matching_titles": matching_titles
                })
    
    else:
        
        return HttpResponseRedirect(reverse("encyclopedia:index"))

def edit(request):
    
    if request.method == "POST":

        entry_title = request.POST.get("entry_title")
        entry = request.POST.get("entry")

        return render(request, "encyclopedia/edit.html", {
            "entry_title": entry_title,
            "entry": entry
        })
    
    else:
        return HttpResponseRedirect(reverse("encyclopedia:index"))
    
def saved(request):
    
    if request.method == "POST":
        
        entry_title = request.POST.get("entry_title")
        entry = request.POST.get("entry")

        util.save_entry(entry_title,entry)

        return render(request, "encyclopedia/saved.html", {
            "entry_title": entry_title
        })
    
    else:
        return HttpResponseRedirect(reverse("encyclopedia:index"))
