from django import forms
from .models import Department,Designation,Location

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['department_name','description']
        widgets = {
            'department_name': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            
            'description': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
           
          
        }

class Designation_Add_Form(forms.ModelForm):

    class Meta:
        model = Designation
        fields = ['department','designation_name', 'description']
        widgets = {
            'department':forms.Select(attrs={'class': 'form-control', 'required': 'true'}),
            'designation_name': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'})
            
           }

    def __init__(self, *args, **kwargs):
        super(Designation_Add_Form, self).__init__(*args, **kwargs)
        self.fields['department'].queryset = Department.objects.all()


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['location_name','description']
        widgets = {
            'location_name': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            
            'description': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
           
          
        }