from django.shortcuts import render
from .forms import LoginUserForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
menu = [
        {'title': "Главная страница", 'url_name': 'movie_list'},
        {'title': "О сайте", 'url_name': 'about'},
        {'title': "Обратная связь", 'url_name': 'contact'},     
]
# Create your views here.
def login_user(request):
    if request.method == 'POST':
        form = LoginUserForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'],
                                password=cd['password'])
            if user and user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('movie_list'))
    else:
        form = LoginUserForm
    return render(request, 'users/login.html', {'form': form})
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('users:login'))

