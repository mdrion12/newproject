from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Donor
from .models import DonationHistory
from .models import DonationHistory

# 🔹 Donor profile form
class DonorForm(forms.ModelForm):
    class Meta:
        model = Donor
        fields = ['blood_group', 'phone', 'department', 'profile_pic', 'available', 'last_donation_date']
        widgets = {
            'last_donation_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'blood_group': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control'}),
            'available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

# 🔹 Registration form (email required)
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="A valid email is required.")

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered")
        return email

# 🔹 Login form (username + password)
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your username'
    }))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your password'
    }))
# forms.py


class DonationHistoryForm(forms.ModelForm):
    class Meta:
        model = DonationHistory
        fields = ['receiver_name', 'location', 'date', 'notes']



