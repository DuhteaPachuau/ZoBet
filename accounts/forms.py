from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-gray-800 border border-gray-700 text-white placeholder-gray-400 focus:border-red-500 focus:ring-1 focus:ring-red-500 outline-none transition', 'placeholder': 'Enter your email'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-gray-800 border border-gray-700 text-white placeholder-gray-400 focus:border-red-500 focus:ring-1 focus:ring-red-500 outline-none transition', 'placeholder': 'Choose a username'}))
    phone = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-gray-800 border border-gray-700 text-white placeholder-gray-400 focus:border-red-500 focus:ring-1 focus:ring-red-500 outline-none transition', 'placeholder': 'Mobile number (optional)'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-gray-800 border border-gray-700 text-white placeholder-gray-400 focus:border-red-500 focus:ring-1 focus:ring-red-500 outline-none transition', 'placeholder': 'Create a password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-gray-800 border border-gray-700 text-white placeholder-gray-400 focus:border-red-500 focus:ring-1 focus:ring-red-500 outline-none transition', 'placeholder': 'Confirm password'}))
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=commit)
        phone = self.cleaned_data.get('phone')
        if phone:
            user.profile.phone = phone
            user.profile.save()
        return user

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-gray-800 border border-gray-700 text-white placeholder-gray-400 focus:border-red-500 focus:ring-1 focus:ring-red-500 outline-none transition', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-gray-800 border border-gray-700 text-white placeholder-gray-400 focus:border-red-500 focus:ring-1 focus:ring-red-500 outline-none transition', 'placeholder': 'Password'}))

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_image', 'phone']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-gray-800 border border-gray-700 text-white placeholder-gray-400 focus:border-red-500 focus:ring-1 focus:ring-red-500 outline-none transition', 'placeholder': 'Phone number'}),
            'profile_image': forms.FileInput(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-gray-800 border border-gray-700 text-white file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-red-500 file:text-white hover:file:bg-red-600 cursor-pointer focus:border-red-500 focus:ring-1 focus:ring-red-500 outline-none transition'}),
        }
