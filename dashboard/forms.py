from django import forms
from .models import Resume
import json


class ResumeForm(forms.ModelForm):
    """Form for building a resume."""
    class Meta:
        model = Resume
        fields = ['full_name', 'email', 'phone', 'address', 'summary', 'skills',
                  'languages', 'hobbies', 'linkedin', 'github']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 3,
                                             'placeholder': 'Brief professional summary...'}),
            'skills': forms.TextInput(attrs={'class': 'form-control',
                                             'placeholder': 'Python, Django, SQL, Communication...'}),
            'languages': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'English, Hindi...'}),
            'hobbies': forms.TextInput(attrs={'class': 'form-control'}),
            'linkedin': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://linkedin.com/in/...'}),
            'github': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://github.com/...'}),
        }

