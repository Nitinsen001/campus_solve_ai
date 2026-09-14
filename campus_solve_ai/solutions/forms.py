from django import forms
from solutions.models import Solution

class SolutionForm(forms.ModelForm):
    class Meta:
        model = Solution
        fields = ['solution_text']
        widgets = {
            'solution_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Describe your solution in detail'}),
        }
