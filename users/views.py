
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .models import *
from .forms import RegisterForm





def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('/admin/')  # Redirect admin to Django admin panel
            else:
                return redirect('dashboard')  # Redirect normal user to dashboard
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})

    return render(request, 'login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

def signup_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


@login_required
def dashboard_view(request):
    if request.user.role == 'provider':
        return render(request, 'provider_dashboard.html')
    elif request.user.role == 'customer':
        return render(request, 'customer_dashboard.html')

    else:
        return redirect('home')

def dashboard(request):
    if request.user.role == 'provider':
        return render(request, 'provider_dashboard.html')
    elif request.user.role == 'customer':
        return render(request, 'customer_dashboard.html')

    else:
        return redirect('home')







