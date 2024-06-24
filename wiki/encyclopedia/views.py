from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django import forms
from . import util


def index(request):
    list = util.list_entries()
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

    list = util.list_entries()
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
    
def inList(n,list):
    name = n.upper()
    listCaps = []

    for i in list:
        listCaps.append(i.upper())
    
    if name in listCaps:
        return True
    else:
        return False