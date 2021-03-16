from django.shortcuts import render
from django import forms
from . import util
import re
import markdown2
from django.http import HttpResponseRedirect
import random



class NewFormAdd(forms.Form):
    titlle = forms.CharField(label="Page Titlle")
    content = forms.CharField(widget=forms.Textarea)
    

def index(request):
    search_name = request.GET.get('q', '')
    if search_name:
        if util.get_entry(search_name):
            content = util.get_entry(search_name)
            return render(request, "encyclopedia/page.html", {
            "page": search_name,
            "content": markdown2.markdown(content)
            })
        else:
            list_entries_search = []
            for page in util.list_entries():
                if re.search('\\b' + search_name, page, re.IGNORECASE):
                    list_entries_search.append(page)
            if not list_entries_search:
                return render(request, "encyclopedia/not_found.html", {
                    "page": search_name
                })
            return render(request, "encyclopedia/index.html", {
                'desc': f'Results for "{search_name}"',
                "entries": list_entries_search
            })
    return render(request, "encyclopedia/index.html", {
        'desc': 'All Pages',
        "entries": util.list_entries()
    })

def add_page(request):
    if request.method == "POST":
        form = NewFormAdd(request.POST)
        if form.is_valid():
            repeatd = False
            titlle = form.cleaned_data["titlle"]
            content = form.cleaned_data["content"]
            for page in util.list_entries():
                if re.search('\\b' + titlle + '\\b', page, re.IGNORECASE):
                    repeatd = True
            if repeatd:
                return render(request, "encyclopedia/add_page.html", {
                    "form": form,
                    'repeatd': repeatd,
                    "url_page": "add_page"
                })
            util.save_entry(titlle, content, True)
            return HttpResponseRedirect("/wiki/" + titlle)

    return render(request, "encyclopedia/add_page.html", {
        "form": NewFormAdd(),
        "url_page": "add_page"
    })

def edit_page(request):
    if request.method == "POST":
        form = NewFormAdd(request.POST)
        if form.is_valid():
            titlle = form.cleaned_data["titlle"]
            content = form.cleaned_data["content"]
            if content:
                util.save_entry(titlle, content, False)
            try:
                return render(request, "encyclopedia/page.html", {
                    "content": markdown2.markdown(util.get_entry(titlle))
                })
            except UnicodeDecodeError:
                return HttpResponseRedirect("/wiki/")
        else:
            return render(request, "tasks/add.html", {
               "form": form
            })
    page = request.GET.get('name', '')
    if page:
        dic_content = {"titlle" : page, "content": util.get_entry(page)}
        return render(request, "encyclopedia/add_page.html", {
            "form": NewFormAdd(dic_content),
            "url_page": "edit_page"
        })
    else:
        return HttpResponseRedirect("/wiki/")

def random_page(request):
    list_pages = util.list_entries()
    return HttpResponseRedirect("/wiki/" + list_pages[random.randint(0,len(list_pages) - 1)])

def pages(request, page):
    if util.get_entry(page):
        content = util.get_entry(page)
        return render(request, "encyclopedia/page.html", {
            "content": markdown2.markdown(content),
            "page": page
        })
    else:
        return render(request, "encyclopedia/not_found.html", {
            "page": page
        })


