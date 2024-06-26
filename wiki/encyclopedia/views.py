from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django import forms
from . import util


import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

class newForm(forms.Form):
    title = forms.CharField(label="Title",widget=forms.TextInput(attrs={'class' : 'in', 'autofocus':'True', 'minlength' : '1'}))
    textarea = forms.CharField(widget=forms.Textarea(attrs={ 'class' : 'text','class' : 'in'}))
    
list = util.list_entries()

def index(request):
    subList = []

    # POST METHOD:
    if  request.method == "POST":
        search = request.POST["q"].strip()
        
        if inList(search,list):
            return HttpResponseRedirect(reverse("wiki:direct", args=[f"{search}"]))
        else:
                for i in list:
                    if i.find(search) > 0:
                        subList.append(i)

                return render(request,"encyclopedia/results.html",{
                    "error": search,
                    "list": subList
                })
    # GET METHOD:

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def direct(request, title):

    titleCaps = title.upper()
    titleLow = title.lower()
    listCaps = []
    for n in list:
        listCaps.append(n.upper())
    
    if inList(title,list):
        index = listCaps.index(f"{titleCaps}")
        return render(request, f"encyclopedia/{titleLow}.html", {
            "content": util.get_entry(list[index])
        })
    else:
        return render(request, "encyclopedia/error.html",{
            "error": title
        })
    
def new(request):

    if request.method == "POST":
        title = request.POST['title'].strip()
        content = request.POST['textarea']

        if inList(title,list):
            print("Error Message/ Error page")
        else:
            util.save_entry(title,content)
            save_entryHtml(title, content)
            return HttpResponseRedirect(reverse("wiki:direct", args=[f"{title}"]))
        
    return render(request,"encyclopedia/new.html", {
        "form": newForm()
    })

# HELPER FUNCTIONS
def inList(n,list):

    name = n.upper()
    listCaps = []

    for i in list:
        listCaps.append(i.upper())
    
    if name in listCaps:
        return True
    else:
        return False
    
def save_entryHtml(title, content):
    
    filename = f"encyclopedia/templates/encyclopedia/{title}.html"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))