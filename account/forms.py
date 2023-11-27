from django import forms
from django.contrib.auth.models import User

class registerForms(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 60rem; border: 1px solid black;'}), label='İsim :')
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 60rem; border: 1px solid black;'}), label='Soyad :')
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 60rem; border: 1px solid black;'}), label='Kullanıcı adı :')
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control', 'style': 'width: 60rem; border: 1px solid black;'}), label='E-posta :')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'style': 'width: 60rem; border: 1px solid black;'}), label='parola :')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'style': 'width: 60rem; border: 1px solid black;'}), label='parola tekrar :')
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2',)



class loginForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 60rem; border: 1px solid black;'}), label='Kullanıcı adı :')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'style': 'width: 60rem; border: 1px solid black;'}), label='parola :')
    class Meta:
        model = User
        fields = ('username', 'password',)
