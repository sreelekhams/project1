from django import forms
from .models import Department

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['department_name','description']
        widgets = {
            'department_name': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            
            'description': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
           
          
        }

  