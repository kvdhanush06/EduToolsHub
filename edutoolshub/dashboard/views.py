from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic

from .forms import (ConversationLengthForm, ConversationMassForm,
                    ConversionForm, DashboardForm, HomeWorkForm, NotesForm,
                    ToDoForm, UserRegistrationForm)
from .models import HomeWork, Notes, Todo
from .services import (convert_length, convert_mass, lookup_dictionary,
                       lookup_wikipedia, search_books, search_youtube)


def home(request):
    context = {
        "username": request.user.username if request.user.is_authenticated else None
    }
    return render(request, "dashboard/home.html", context)


@login_required
def notes(request):
    if request.method == "POST":
        form = NotesForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            messages.success(request, "Note added successfully")
            return redirect("notes")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = NotesForm()

    notes_qs = Notes.objects.filter(user=request.user)
    context = {"notes": notes_qs, "form": form}
    return render(request, "dashboard/notes.html", context)


@login_required
def delete_note(request, pk=None):
    # Only delete if the note belongs to the requesting user
    note = get_object_or_404(Notes, id=pk, user=request.user)
    note.delete()
    return redirect("notes")


class NotesDetailView(generic.DetailView):
    model = Notes


@login_required
def homework(request):
    if request.method == "POST":
        form = HomeWorkForm(request.POST)
        if form.is_valid():
            hw = form.save(commit=False)
            hw.user = request.user
            hw.save()
            messages.success(request, "Homework added successfully")
            return redirect("homework")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = HomeWorkForm()

    homeworks = HomeWork.objects.filter(user=request.user)
    homework_done = len(homeworks) == 0
    context = {
        "homeworks": homeworks,
        "homework_done": homework_done,
        "form": form,
    }
    return render(request, "dashboard/homework.html", context)


@login_required
def update_homework(request, pk=None):
    homework = get_object_or_404(HomeWork, id=pk, user=request.user)
    homework.is_finished = not bool(homework.is_finished)
    homework.save()
    return redirect("homework")


@login_required
def delete_homework(request, pk=None):
    hw = get_object_or_404(HomeWork, id=pk, user=request.user)
    hw.delete()
    return redirect("homework")


@login_required
def youtube(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data.get("text", "")
            result_list = search_youtube(text, limit=10)
            context = {"form": form, "results": result_list}
            return render(request, "dashboard/youtube.html", context)
        messages.error(request, "Please enter a search term.")
    else:
        form = DashboardForm()

    context = {"form": form}
    return render(request, "dashboard/youtube.html", context)


@login_required
def todo(request):
    if request.method == "POST":
        form = ToDoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            messages.success(request, "Todo added successfully")
            return redirect("todo")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ToDoForm()

    todos = Todo.objects.filter(user=request.user)
    todos_done = len(todos) == 0
    context = {
        "form": form,
        "todos": todos,
        "todos_done": todos_done,
    }
    return render(request, "dashboard/todo.html", context)


@login_required
def update_todo(request, pk=None):
    todo = get_object_or_404(Todo, id=pk, user=request.user)
    todo.is_finished = not bool(todo.is_finished)
    todo.save()
    return redirect("todo")


@login_required
def delete_todo(request, pk=None):
    todo = get_object_or_404(Todo, id=pk, user=request.user)
    todo.delete()
    return redirect("todo")


@login_required
def books(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data.get("text", "")
            result_list = search_books(text, limit=10)
            context = {"form": form, "results": result_list}
            return render(request, "dashboard/books.html", context)
        messages.error(request, "Please enter a search term.")
    else:
        form = DashboardForm()

    context = {"form": form}
    return render(request, "dashboard/books.html", context)


@login_required
def dictionary(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data.get("text", "")
            details = lookup_dictionary(text)
            if details:
                context = {"form": form, "input": text, **details}
            else:
                context = {"form": form, "input": ""}
            return render(request, "dashboard/dictionary.html", context)
        messages.error(request, "Please enter a search term.")
    else:
        form = DashboardForm()
        context = {"form": form}
    return render(request, "dashboard/dictionary.html", context)


@login_required
def wiki(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data.get("text", "")
            # use full text for lookup; lookup_wikipedia will sanitize/shorten
            context = {"form": form, **lookup_wikipedia(text)}
            return render(request, "dashboard/wiki.html", context)
        messages.error(request, "Please enter a search term.")
    else:
        form = DashboardForm()
        context = {"form": form}
    return render(request, "dashboard/wiki.html", context)


@login_required
def conversion(request):
    if request.method == "POST":
        form = ConversionForm(request.POST)
        if form.is_valid():
            measurement = form.cleaned_data.get("measurement")
            if measurement == "length":
                measurement_form = ConversationLengthForm(request.POST)
                context = {"form": form, "m_form": measurement_form, "input": True}
                if measurement_form.is_valid():
                    inp = measurement_form.cleaned_data.get("input")
                    first = measurement_form.cleaned_data.get("measure1")
                    second = measurement_form.cleaned_data.get("measure2")
                    answer = ""
                    if inp is not None:
                        converted = convert_length(inp, first, second)
                        answer = converted or ""
                    context["answer"] = answer
            elif measurement == "mass":
                measurement_form = ConversationMassForm(request.POST)
                context = {"form": form, "m_form": measurement_form, "input": True}
                if measurement_form.is_valid():
                    inp = measurement_form.cleaned_data.get("input")
                    first = measurement_form.cleaned_data.get("measure1")
                    second = measurement_form.cleaned_data.get("measure2")
                    answer = ""
                    if inp is not None:
                        converted = convert_mass(inp, first, second)
                        answer = converted or ""
                    context["answer"] = answer
            else:
                context = {"form": form, "input": False}
        else:
            messages.error(request, "Please correct the errors in the form.")
    else:
        form = ConversionForm()
        context = {"form": form, "input": False}
    return render(request, "dashboard/conversion.html", context)


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Account Created for {username}")
            return redirect("login")
    else:
        form = UserRegistrationForm()
    context = {"form": form}
    return render(request, "dashboard/register.html", context)


@login_required
def profile(request):
    homeworks = HomeWork.objects.filter(is_finished=False, user=request.user)
    todos = Todo.objects.filter(is_finished=False, user=request.user)

    homework_done = True if len(homeworks) == 0 else False
    todos_done = True if len(todos) == 0 else False
    context = {
        "homeworks": homeworks,
        "todos": todos,
        "homework_done": homework_done,
        "todos_done": todos_done,
    }

    return render(request, "dashboard/profile.html", context)
