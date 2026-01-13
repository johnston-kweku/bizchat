from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Business, Services, Products

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 =forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name','username', 'email'
        ]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password and password2 and password != password2:
            raise forms.ValidationError("Passwords do not match")
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists.")
        return email
    

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'bio', 'profile_picture',
        ]

class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = [
            'title'
        ]

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Services
        fields = [
            'title', 'description'
        ]

class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = [
            'title', 'description', 'image'
        ]
    