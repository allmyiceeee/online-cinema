from django.shortcuts import render, get_object_or_404, redirect
from .forms import LoginUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from users.forms import RegisterUserForm
from django.views.generic import CreateView
from .models import Wishlist
from first.models import Movie
from django.contrib.auth.decorators import login_required
# Create your views here.

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}
    
    def get_success_url(self):
        return reverse_lazy('movie_list')

def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('users:login'))
class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': 'Регистрация'}
    success_url = reverse_lazy('users:login')
    
    

def register(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(form.cleaned_data['password'])
            user.save()
            return render(request,'users/register_done.html') 
    form = RegisterUserForm()
    return render(request, 'users/register.html', {'form': form})

def profile(request):
    return render(request, 'profile.html')

@login_required
def wishlist_view(request, type):
    wishlist_movie = Wishlist.objects.filter(user=request.user, wishlist_type=type).select_related('movie')
    movies = [i.movie for i in wishlist_movie]
    
    return render(request, 'users/wishlist.html', {
        'wishlist_type': type, 
        'movies': movies,
        })
    

@login_required
def add_to_wishlist(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    if request.method == 'POST':
        wishlist_type = request.POST.get('wishlist_type')
        
        existing = Wishlist.objects.filter(user=request.user, movie=movie, wishlist_type=wishlist_type)
        if not existing.exists():
            Wishlist.objects.create(user=request.user, movie=movie, wishlist_type=wishlist_type)
    return redirect('movie_detail', movie_id=movie.id)