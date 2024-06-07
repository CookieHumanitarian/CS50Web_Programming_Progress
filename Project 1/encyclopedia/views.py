import random
import markdown2
from django.shortcuts import render
from django import forms
from . import util
from django.shortcuts import redirect

class searchBar(forms.Form):
    task = forms.CharField(label="Search Encyclopedia")
    
class addForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput)
    description = forms.CharField(widget=forms.Textarea(attrs={'style': "width: 100%"}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "search": searchBar()
    })      

def title(request, name):
    return render(request, "encyclopedia/title.html", {
        "title": name,
        "page": markdown2.markdown(util.get_entry(name)),
        "search": searchBar()
    })

def search(request):
    if request.method == "POST":
        tasks = []
        form = searchBar(request.POST)
        if form.is_valid():
            task = form.cleaned_data["task"]
            entries = util.list_entries()
            for entry in entries:
                if task.lower() == entry.lower():
                    return redirect('tasks:title', name=task)
    
                if task.lower() in entry.lower():
                    tasks.append(entry)
            
            if not tasks:
                return redirect('tasks:index')
          
            return render(request, "encyclopedia/index.html", {
                "entries": tasks,
                "search": searchBar()
            })

    if request.method == "GET":
        return redirect('tasks:index')

def create(request):
    if request.method == "POST":
         form = addForm(request.POST)
         if form.is_valid():
            head = form.cleaned_data['title']
            content = form.cleaned_data['description']
            check_existing = util.get_entry(head)
            if check_existing is None:
                util.save_entry(head, content)
                return redirect('tasks:title', name=head)
            
            else:
                return render(request, "encyclopedia/error.html", {
                    "error": "Page already exists",
                    "search": searchBar()
                })
                
                         
    return render(request, "encyclopedia/create.html", {
        "title": "Add a New Page",
        "page": addForm(),
        "search": searchBar()
    })
    
    
def edit(request, name):
    if request.method == "POST":
        form = addForm(request.POST)
        if form.is_valid():
            head = form.cleaned_data['title']
            content = form.cleaned_data['description']
            util.save_entry(head, content)
            return redirect('tasks:title', name=head)
        
    else:  
        initial_data = {
            "title": name,
            "description": util.get_entry(name),
        }
        edit_form = addForm(initial=initial_data)
        return render(request, "encyclopedia/edit.html", {
            "form": edit_form,
            "search": searchBar()
        })

def random_page(request):
    entries = util.list_entries()
    final_entry = random.choice(entries)
    return redirect('tasks:title', name=final_entry)
    
    