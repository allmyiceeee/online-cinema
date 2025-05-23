from django import forms

class LoginUserForm(forms.Form):
    username = forms.CharField(label='Логин', 
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', 
                            widget=forms.PasswordInput(attrs={'class': 'form-control'}))