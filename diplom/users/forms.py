from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model
from .models import Wishlist
class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', 
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', 
                            widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = get_user_model()
        fields = ['username', 'password']
        
class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput())
    
    class Meta:
        model = get_user_model()
        fields = ['username', 'email','first_name', 'last_name','password1', 'password2']
        labels = {
            'email': 'Email',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }
        

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким email уже существует')
        return email
    
class WishlistForm(forms.ModelForm):
    class Meta:
        model = Wishlist
        fields = ['wishlist_type']