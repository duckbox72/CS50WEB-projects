from django import forms
from django.contrib import messages
#from django.http import HttpResponseRedirect
from django.shortcuts import render
#from django.urls import reverse
from random import randint

import markdown2

from . import util


# CREATE VIEWS BELOW.
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def addentry(request):    
    # User reaches via GET request
    if request.method == "GET":
        return render(request, "encyclopedia/addentry.html")

    # User reaches via POST request
    else:
        # Check if a title was submitted
        title = request.POST.get("title")
        if not title:
            return render(request, "encyclopedia/addentry.html") 
        
        # Check if text was submitted
        text = request.POST.get("text")
        if not text:
            return render(request, "encyclopedia/addentry.html") 
        
        # Check if there is already an entry with submitted title
        entry = util.get_entry(title)
        if entry != None:
            return render(request, "encyclopedia/alreadyexists.html", {
                "title": title,
            })
        
        # Save new entry to disk and go to entry page
        util.save_entry(title, text)
        return render(request, "encyclopedia/entry.html", {
                "name": title.capitalize(),
                "entry": markdown2.markdown(text)
            })


def editentry(request):
        # Handle POST request via entry page (case name exists)
        name = request.POST.get("name")
        if name != None:
            entry = util.get_entry(name)
            return render(request, "encyclopedia/editentry.html", {
                "name": name,
                "entry": entry
            })
        else:
            # Handle POST request via editentry page
            title = request.POST.get("title")
            text = request.POST.get("text")

            # Save updated entry to disk and go to entry page
            util.save_entry(title, text)
            return render(request, "encyclopedia/entry.html", {
                "name": title,
                "entry": markdown2.markdown(text)
            })

            
def entry(request, name):  
    # User reaches via GET request (using address bar)
    if request.method == "GET":      
        # Render an apology case entry does not exist
        if util.get_entry(name) == None:
            return render(request, "encyclopedia/apology.html", {
                "name": name
            })
        # Render entry page in markdown format
        else:
            entry = util.get_entry(name)
            return render(request, "encyclopedia/entry.html", {
                "name": name,
                "entry": markdown2.markdown(entry)
            })
    # User reaches via POST request (using the search bar)
    else:
        name = request.POST.get("q")

        # Chech if there are entries that match query string (name) 
        if util.get_entry(name) == None:
            entries = []
            allentries = util.list_entries()
            
            # Compare and list substrings if no entries were found
            for entry in allentries:
                if name.lower() in entry.lower():
                    entries.append(entry)
            
            if entries == []:
                noresult = "Your search returned no results. Please try again."
            
            else:
                noresult = ""
            
            return render(request, "encyclopedia/searchresults.html", {
                "entries": entries,
                "noresult": noresult
            })
        # Case name matches an entry
        else:
            entry = util.get_entry(name)
            
            return render(request, "encyclopedia/entry.html", {
                "name": name,
                "entry": markdown2.markdown(entry)
            })


def random(request):
    entries = util.list_entries()
    name = entries[randint(0, len(entries)-1)]
    entry = util.get_entry(name)

    return render(request, "encyclopedia/entry.html", {
                "name": name,
                "entry": markdown2.markdown(entry)
    })