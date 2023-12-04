from django import forms
from django.contrib.auth.models import User
from account.models import UserProfile
from ckeditor.widgets import CKEditorWidget

class registerForms(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 27rem; border: 1px solid black;'}), label='Kullanıcı adı :')
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control', 'style': 'width: 27rem; border: 1px solid black;'}), label='E-posta :')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'style': 'width: 13rem; border: 1px solid black;'}), label='parola :')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'style': 'width: 13rem; border: 1px solid black;'}), label='parola tekrar :')
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2',)



class loginForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 20rem; border: 1px solid black;'}), label='Kullanıcı adı :')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'style': 'width: 20rem; border: 1px solid black;'}), label='parola :')
    class Meta:
        model = User
        fields = ('username', 'password',)




class profileForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control' }), label='Kullanıcı adı:', required=False)
    profile_picture = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}), label='profil fotoğrafı: ',required=False)
    about = forms.CharField(widget=CKEditorWidget(attrs={'class': 'form-control'}), label='hakkında:', required=False)
    class Meta:
        model = UserProfile
        fields = ('username', 'profile_picture', 'about',)
