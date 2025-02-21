from django import forms
from .models import PulseChatUsers, Group

class UserForm(forms.ModelForm):
    class Meta:
        model = PulseChatUsers
        fields = ['username','full_name','email','password','bio']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'username','class': 'form-control mb-4'}),
            'full_name': forms.TextInput(attrs={'placeholder': 'Full Name','class': 'form-control mb-4'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email','class': 'form-control mb-4'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Strong Password','class': 'form-control mb-4'}),
            'bio': forms.TextInput(attrs={'placeholder': 'Optoinal!','class': 'form-control mb-4'}),
        }


class CreateGroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name','description']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter a Unique Name...','class': 'form-control mb-4'}),
            'description': forms.TextInput(attrs={'placeholder': 'Describe Your Group...','class': 'form-control mb-4'}),
        }