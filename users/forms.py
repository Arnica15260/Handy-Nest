

from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms
from .models import TeachingRequest, NursingService,  VolunteeringService

#RegisterForm
class RegisterForm(UserCreationForm):
    phone_number = forms.CharField(required=True, max_length=11)

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'phone_number','password1', 'password2']


#TeachingService
class TeachingRequestForm(forms.ModelForm):
    class Meta:
        model = TeachingRequest
        fields = ['customer','title','subject','description','location','is_paid']

#NursingService
class NursingServiceForm(forms.ModelForm):
    class Meta:
        model = NursingService
        fields = ['customer','title','description','location','is_paid']

#VolunteeringService
class VolunteeringServiceForm(forms.ModelForm):
    class Meta:
        model = VolunteeringService
        fields = ['customer','title','activity','location','is_paid']




