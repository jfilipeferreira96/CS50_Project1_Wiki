from tkinter import Entry
from django.shortcuts import render, redirect
from . import util
import random
from markdown2 import Markdown
from django import forms
from random import randint

markdowner = Markdown()


class NewEntryForm(forms.Form):
    # Create a new entry form:
    form_title = forms.CharField(label="Title", min_length=1, max_length=20, widget=forms.TextInput(
        attrs={'placeholder': "Insert a title", 'class': 'form-control mt-1', 'id': 'inputTitle'}))
    form_textarea = forms.CharField(label="Description", min_length=1, widget=forms.Textarea(
        attrs={'rows': '15', 'cols': '15', 'placeholder': "Insert a description", 'class': 'form-control mt-1', 'id': 'textArea'}))


class EditEntryForm(forms.Form):
    form_title = forms.CharField(required=False, label="Title", min_length=1, max_length=20, widget=forms.TextInput(
        attrs={'disabled': 'true', 'placeholder': "Insert a title", 'class': 'form-control mt-1', 'id': 'inputTitle'}))
    form_textarea = forms.CharField(label="Description", min_length=1, widget=forms.Textarea(
        attrs={'rows': '15', 'cols': '15', 'placeholder': "Insert a description", 'class': 'form-control mt-1', 'id': 'textArea'}))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def title(request, entry_title):
    if util.get_entry(entry_title) is not None:
        return render(request, "encyclopedia/entry.html", {
            "entry_title": entry_title,
            "entry_content": markdowner.convert(util.get_entry(entry_title))
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "message": "Oops, something went wrong!"
        })


def new(request):
    if request.method == "POST":

        form = NewEntryForm(request.POST)
        entries = util.list_entries()

        if form.is_valid():
            form_title = form.cleaned_data["form_title"]
            form_textarea = form.cleaned_data["form_textarea"]
            # Check if already exists this entry
            if form_title in entries:
                return render(request, "encyclopedia/error.html", {
                    "message": "This topic already exists!"
                })
            else:
                # Saves the entry
                util.save_entry(form_title, f"#{form_title}\n" + form_textarea)
                return redirect('/wiki/' + form_title)
    else:
        return render(request, "encyclopedia/new.html", {
            "form": NewEntryForm()
        })


def edit(request, entry_title):
    if request.method == "POST":
        form = EditEntryForm(request.POST)
        if form.is_valid():
            form_textarea = form.cleaned_data["form_textarea"]
            # Saves the edited content
            util.save_entry(entry_title, form_textarea)
            return redirect('/wiki/' + entry_title)
    else:
        # Sends the user to the edit page
        if util.get_entry(entry_title) is not None:
            editform = EditEntryForm(
                {"form_title": entry_title, "form_textarea": util.get_entry(entry_title)})
            return render(request, "encyclopedia/edit.html", {"entry_title": entry_title, "editform": editform})
        else:
            return render(request, "encyclopedia/error.html", {
                "message": "Oops, something went wrong!"
            })


def random(request):
    listof_entries = util.list_entries()
    if len(listof_entries) > 0:
        random_num = randint(0, len(listof_entries) - 1)
        random_entrie = listof_entries[random_num]
        return redirect('/wiki/' + random_entrie)
    else:
        return redirect("encyclopedia/error.html", {
            "message": "There are no entries!"
        })


def search_entry(request):
    if request.method == "POST":
        query = request.POST["q"].lower()
        words_filtered = []

        for entry in util.list_entries():
            # if the query contains the some letters of the entry
            if query in entry.lower():
                words_filtered.append(entry)
                # if the query matches perfectly
                if query == entry.lower():
                    return redirect('/wiki/' + entry)
        if len(words_filtered) >= 1:
            return render(request, "encyclopedia/index.html", {
                "entries": words_filtered
            })
        else:
            return render(request, "encyclopedia/error.html", {
                "message": "Such word does not exists in our database. Feel free to add it."
            })
