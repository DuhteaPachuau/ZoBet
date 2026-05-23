from django import forms
from .models import Event, Team

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'banner', 'entry_fee', 'commission_percentage', 'prediction_deadline', 'start_date', 'end_date', 'featured', 'max_participants', 'status']
        labels = {'entry_fee': 'Minimum Bet (₹)'}
        input_class = 'w-full px-4 py-3 rounded-xl bg-gray-800 border border-gray-700 text-white placeholder-gray-400 focus:border-red-500 focus:ring-1 focus:ring-red-500 outline-none transition'
        file_class = 'w-full px-4 py-3 rounded-xl bg-gray-800 border border-gray-700 text-white file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-red-500 file:text-white hover:file:bg-red-600 cursor-pointer focus:border-red-500 focus:ring-1 focus:ring-red-500 outline-none transition'
        select_class = 'w-full px-4 py-3 rounded-xl bg-gray-800 border border-gray-700 text-white focus:border-red-500 focus:ring-1 focus:ring-red-500 outline-none transition'
        widgets = {
            'title': forms.TextInput(attrs={'class': input_class}),
            'description': forms.Textarea(attrs={'class': input_class, 'rows': 4}),
            'banner': forms.FileInput(attrs={'class': file_class}),
            'entry_fee': forms.NumberInput(attrs={'class': input_class}),
            'commission_percentage': forms.NumberInput(attrs={'class': input_class}),
            'prediction_deadline': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': input_class}),
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': input_class}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': input_class}),
            'featured': forms.CheckboxInput(attrs={'class': 'w-4 h-4 text-red-500 bg-gray-800 border-gray-700 rounded focus:ring-red-500'}),
            'max_participants': forms.NumberInput(attrs={'class': input_class}),
            'status': forms.Select(attrs={'class': select_class}),
        }

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'logo', 'description', 'short_code']
        input_class = 'w-full px-4 py-3 rounded-xl bg-gray-800 border border-gray-700 text-white placeholder-gray-400 focus:border-red-500 focus:ring-1 focus:ring-red-500 outline-none transition'
        file_class = 'w-full px-4 py-3 rounded-xl bg-gray-800 border border-gray-700 text-white file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-red-500 file:text-white hover:file:bg-red-600 cursor-pointer focus:border-red-500 focus:ring-1 focus:ring-red-500 outline-none transition'
        widgets = {
            'name': forms.TextInput(attrs={'class': input_class}),
            'logo': forms.FileInput(attrs={'class': file_class}),
            'description': forms.Textarea(attrs={'class': input_class, 'rows': 3}),
            'short_code': forms.TextInput(attrs={'class': input_class}),
        }
