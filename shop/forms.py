from django import forms
from django.contrib.auth.models import User
from .models import UserInfo

class UserForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta():
        model = User
        fields = ('username', 'email', 'password')

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class ExtendedUserForm(forms.ModelForm):

    class Meta():
        model = UserInfo
        fields = ('address', 'state', 'city', 'pincode', 'phone')
        # fields = '__all__'
        widgets = {
            'address': forms.TextInput(attrs={'class':'form-control'}),
            'state': forms.TextInput(attrs={'class':'form-control'}),
            'city': forms.TextInput(attrs={'class':'form-control'}),
            'pincode': forms.TextInput(attrs={'class':'form-control'}),
            'phone': forms.TextInput(attrs={'class':'form-control'})
        }