from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def direct(request, title):
    list = util.list_entries()
    listCaps = []
    for n in list:
        listCaps.append(n.upper())

    if title.upper() in listCaps:
        index = listCaps.index(f"{title.upper()}")
        print(title.lower())
        return render(request, f"encyclopedia/{title.lower()}.html", {
            "content": util.get_entry(list[index])
        })
    else:
        return render(request, "encyclopedia/error.html",{
            "error": title
        })