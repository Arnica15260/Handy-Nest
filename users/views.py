
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import RegisterForm, TeachingRequestForm, ContactForm
from .models import TeachingRequest, NursingService, VolunteeringService
from .forms import TeachingRequest, NursingServiceForm, VolunteeringServiceForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ContactForm
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.shortcuts import redirect
from django.conf import settings
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
import os
from .models import ProviderProfile







#For login
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('/admin/')
            else:
                return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})

    return render(request, 'login.html')

#For logout
@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

#for registration
def signup_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.phone_number = form.cleaned_data['phone_number']
            user.save()
            return redirect('user_login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


#for dashboard
@login_required
def dashboard_view(request):
    if request.user.role == 'provider':
        teaching_requests = TeachingRequest.objects.all()
        return render(request, 'provider_dashboard.html', {
            'teaching_requests': teaching_requests
        })
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





@login_required
def teaching_service_view(request):
    if request.method == 'POST':
        form = TeachingRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = TeachingRequestForm()

    teaching_requests = TeachingRequest.objects.all()
    return render(request, 'teaching.html', {
        'form': form,
        'teaching_requests': teaching_requests
    })


@login_required
def nursing_service_view(request):
    if request.method == 'POST':
        form = NursingServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = NursingServiceForm()
    return render(request, 'nursing.html', {'form': form})

@login_required
def volunteering_service_view(request):
    if request.method == 'POST':
        form = VolunteeringServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = VolunteeringServiceForm()
    return render(request, 'volunteering.html', {'form': form})

@login_required
def provider_dashboard(request):
    teaching_requests = TeachingRequest.objects.filter(customer__role='customer')

    return render(request, 'provider_dashboard.html', {
        'teaching_requests': teaching_requests
    })

@login_required
def provider_teaching_posts(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        action = request.POST.get('action')
        post = get_object_or_404(TeachingRequest, id=post_id)
        if post.status == 'Pending':
            post.status = 'Accepted' if action == 'accept' else 'Rejected'
            post.accepted_by = request.user
            post.save()
        return redirect('provider_teaching_posts')
    posts = TeachingRequest.objects.all()
    return render(request, 'provider_teaching_posts.html', {'posts': posts})


@login_required
def provider_nursing_posts(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        action = request.POST.get('action')
        post = get_object_or_404(NursingService, id=post_id)
        if post.status == 'Pending':
            post.status = 'Accepted' if action == 'accept' else 'Rejected'
            post.accepted_by = request.user
            post.save()
        return redirect('provider_nursing_posts')
    posts = NursingService.objects.all()
    return render(request, 'provider_nursing_posts.html', {'posts': posts})


@login_required
def provider_volunteering_posts(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        action = request.POST.get('action')
        post = get_object_or_404(VolunteeringService, id=post_id)
        if post.status == 'Pending':
            post.status = 'Accepted' if action == 'accept' else 'Rejected'
            post.accepted_by = request.user
            post.save()
        return redirect('provider_volunteering_posts')
    posts = VolunteeringService.objects.all()
    return render(request, 'provider_volunteering_posts.html', {'posts': posts})

@login_required
def my_accepted_posts(request):
    teaching = TeachingRequest.objects.filter(accepted_by=request.user, status='Accepted')
    nursing = NursingService.objects.filter(accepted_by=request.user, status='Accepted')
    volunteering = VolunteeringService.objects.filter(accepted_by=request.user, status='Accepted')

    return render(request, 'provider_my_accepted_posts.html', {
        'teaching_posts': teaching,
        'nursing_posts': nursing,
        'volunteering_posts': volunteering
    })

@login_required
def customer_my_requests(request):
    teaching_posts = TeachingRequest.objects.filter(customer=request.user)
    nursing_posts = NursingService.objects.filter(customer=request.user)
    volunteering_posts = VolunteeringService.objects.filter(customer=request.user)

    return render(request, 'customer_my_requests.html', {
        'teaching_posts': teaching_posts,
        'nursing_posts': nursing_posts,
        'volunteering_posts': volunteering_posts
    })

#update & delete of teaching post
def update_teaching_post(request, pk):
    post = get_object_or_404( TeachingRequest, pk=pk, customer=request.user)
    if request.method == "POST":
        form = TeachingRequestForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('customer_my_requests')
    else:
        form = TeachingRequestForm(instance=post)
    return render(request, 'update.html', {'form': form, 'post': post})

def delete_teaching_post(request, pk):
    post = get_object_or_404(TeachingRequest, pk=pk, customer=request.user)
    if request.method == "POST":
        post.delete()
        return redirect('customer_my_requests')
    return render(request, 'delete.html', {'post': post})



# update & delete for nursing post
def update_nursing_post(request, pk):
    post = get_object_or_404( NursingService, pk=pk, customer=request.user)
    if request.method == "POST":
        form = NursingServiceForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('customer_my_requests')
    else:
        form = NursingServiceForm(instance=post)
    return render(request, 'update.html', {'form': form, 'post': post})

def delete_nursing_post(request, pk):
    post = get_object_or_404(NursingService, pk=pk, customer=request.user)
    if request.method == "POST":
        post.delete()
        return redirect('customer_my_requests')
    return render(request, 'delete.html', {'post': post})

# update & delete for volunteering post
def update_volunteering_post(request, pk):
    post = get_object_or_404( VolunteeringService, pk=pk, customer=request.user)
    if request.method == "POST":
        form = VolunteeringServiceForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('customer_my_requests')
    else:
        form = VolunteeringServiceForm(instance=post)
    return render(request, 'update.html', {'form': form, 'post': post})

def delete_volunteering_post(request, pk):
    post = get_object_or_404(VolunteeringService, pk=pk, customer=request.user)
    if request.method == "POST":
        post.delete()
        return redirect('customer_my_requests')
    return render(request, 'delete.html', {'post': post})



def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')
        else:
            print("Form is not valid:", form.errors)
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})









