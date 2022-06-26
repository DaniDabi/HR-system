from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm


def login_user(request):
    if request.method == "POST":
        uid = request.POST['username']
        pwd = request.POST['password']
        user = authenticate(request, username=uid, password=pwd)
        if user is not None:
            login(request, user)
            messages.success(request, ("You are Successfully Login"))
            return redirect('home' )
        else:
            messages.success(request, ("There Was An Error Logging In, Try Again!! "))
            return redirect('login')
    else:
        return render(request, 'authenticate/login.html',{})

def logout_user(request):
    logout(request)
    messages.success(request, ("You Were Logged out.."))
    return redirect('home')

def register_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            uid = form.cleaned_data['username']
            pwd = form.cleaned_data['password1']
            user = authenticate(request, username=uid, password=pwd)
            login(request, user)
            messages.success(request, ("You are Successfully Signed Up"))
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'authenticate/register_user.html', {
        'form':form,
    })

def HomeView(request):
    return render(request, 'authenticate/home.html', {})



