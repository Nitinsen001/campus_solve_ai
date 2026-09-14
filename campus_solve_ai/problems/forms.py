from django import forms
from problems.models import Problem

class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = ['title', 'description', 'location', 'category', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Brief problem title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Describe the problem in detail'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Hostel Block A, Room 204'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

class AdminProblemEditForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = ['title', 'description', 'location', 'category', 'priority', 'status', 'is_duplicate', 'duplicate_of']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'is_duplicate': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'duplicate_of': forms.Select(attrs={'class': 'form-select'}),
        }
