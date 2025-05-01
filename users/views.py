from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from .middlewares import auth,guest





# Create your views here.
@guest
def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        initial_data = {'username':'','email':'', 'password1':'', 'password2':''}
        form = UserCreationForm(initial=initial_data)

    return render(request, 'register.html', {'form': form})
@guest
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request,data= request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        initial_data = {'username':'','password':''}
        form = AuthenticationForm(initial=initial_data)
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')
@auth
def dashboard_view(request):
    return render(request,'dashboard.html')

