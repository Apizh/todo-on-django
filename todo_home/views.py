from django.contrib.auth import authenticate, login as loginUser, logout, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from todo_home.forms import TodoUserForm
from todo_home.models import TodoUser
from django.contrib.auth.decorators import login_required


@login_required(login_url='todo_home:login')
def home(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        user = request.user
        form = TodoUserForm()
        todos = TodoUser.objects.filter(user=user)
        return render(request, 'todo_home/index.html', context={'form': form, 'todos': todos})


def login(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        form = AuthenticationForm()
        context = {
            'form': form
        }  # No data needed for this view
        return render(request, 'todo_home/login.html', context=context)
    else:
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                loginUser(request, user)
                return redirect('todo_home:home_page')
        else:
            context = {
                'form': form
            }
            return render(request, 'todo_home/login.html', context=context)


def signup(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        form = UserCreationForm()
        context = {'form': form}
        return render(request, 'todo_home/signup.html', context=context)
    else:  # For debugging purposes
        form = UserCreationForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            user = form.save()
            if user is not None:
                return redirect('todo_home:home_page')
        else:
            return render(request, 'todo_home/signup.html', context=context)


@login_required(login_url='todo_home:login')
def add_todo(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        user = request.user
        form = TodoUserForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            todo = form.save(commit=False)
            todo.user = user
            todo.save()
            print(todo)  # For debugging purposes
            return redirect('todo_home:home_page')
        else:
            return render('todo_home/index.html', {'form': form})


def signout(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect('todo_home:login')
