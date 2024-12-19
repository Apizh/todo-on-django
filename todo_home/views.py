from django.contrib.auth import authenticate, login as login_user, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from todo_home.forms import TodoUserForm
from todo_home.models import TodoUser


def page_not_found(request: HttpRequest, exception):
    """Страница, вызываемая при обращении к несуществующей странице."""
    return render(request, 'todo_home/Not_found_404.html')


@login_required(login_url='todo_home:login')
def home(request: HttpRequest) -> HttpResponse:
    """Главная страница с задачами текущего пользователя."""
    form = TodoUserForm()
    todos = TodoUser.objects.filter(user=request.user)
    return render(request, 'todo_home/index.html', context={'form': form, 'todos': todos})


def login(request: HttpRequest) -> HttpResponse:
    """Страница авторизации пользователя."""
    form = AuthenticationForm(data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = authenticate(
            username=form.cleaned_data.get('username'),
            password=form.cleaned_data.get('password'),
        )
        if user:
            login_user(request, user)
            return redirect('todo_home:home_page')
    return render(request, 'todo_home/login.html', {'form': form})


def signup(request: HttpRequest) -> HttpResponse:
    """Страница регистрации нового пользователя."""
    form = UserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        if user:
            login_user(request, user)
            return redirect('todo_home:home_page')
    return render(request, 'todo_home/signup.html', {'form': form})


@login_required(login_url='todo_home:login')
def add_todo(request: HttpRequest) -> HttpResponse:
    """Добавление новой задачи для текущего пользователя."""
    form = TodoUserForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        todo = form.save(commit=False)
        todo.user = request.user
        todo.save()
        return redirect('todo_home:home_page')
    todos = TodoUser.objects.filter(user=request.user)
    return render(request, 'todo_home/index.html', {'form': form, 'todos': todos})


def signout(request: HttpRequest) -> HttpResponse:
    """Выход пользователя из системы."""
    logout(request)
    return redirect('todo_home:login')


@login_required(login_url='todo_home:login')
def delete_todo(request: HttpRequest, id: int) -> HttpResponse:
    """Удаление задачи, если она принадлежит текущему пользователю."""
    todo = get_object_or_404(TodoUser, pk=id, user=request.user)
    todo.delete()
    return redirect('todo_home:home_page')
