
from django.shortcuts import render

def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def services(request):
    return render(request, 'services.html')

def contact(request):
    return render(request, 'contact.html')

def login(request):
    return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')




