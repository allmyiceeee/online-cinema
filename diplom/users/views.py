from django.shortcuts import render, get_object_or_404, redirect
from .forms import LoginUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from users.forms import RegisterUserForm
from django.views.generic import CreateView
from .models import Wishlist,WatchedMovie, Rating, Purchase
from first.models import Movie
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta
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

@login_required
def add_to_watched(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    
    WatchedMovie.objects.get_or_create(user=request.user, movie=movie)
    return redirect('movie_detail', movie_id=movie.id)

@login_required
def watched_movies_view(request):
    watched = WatchedMovie.objects.filter(user=request.user).select_related('movie')
    movies = [entry.movie for entry in watched]
    
    return render(request, 'users/watched_movies.html', {
        'movies': movies
        })
    
@login_required
def rate_movie(request, movie_id, value):
    movie = get_object_or_404(Movie, id=movie_id)
    if value not in ['Нравится', 'Не нравится']:
        return redirect('movie_detail',movie_id=movie_id)
    rating_value = 1 if value == 'Нравится' else 2
    
    Rating.objects.update_or_create(
        user=request.user,
        movie=movie,
        defaults={'rating': rating_value}
    )
    return redirect('movie_detail', movie_id=movie.id)

@login_required
def rated_movies_view(request):
    ratings = Rating.objects.filter(user=request.user).select_related('movie')
    
    return render(request, 'users/rated_movies.html', {
        'ratings': ratings
        })

@login_required
def purchase_history(request):
    purchases = Purchase.objects.filter(user=request.user).select_related('movie')
    return render(request, 'users/purchase_history.html', {'purchases': purchases})

@login_required
def buy_ticket(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if request.method == 'POST':
        purchase_type = request.POST.get('purchase_type')
        quantity = int(request.POST.get('quantity', 1))
        price = Decimal('250.00') if purchase_type == 'cinama' else Decimal('100.00')
        
        session_time = None
        if purchase_type == 'cinama':
            session_time = timezone.now() + timedelta(days=3)
        
        Purchase.objects.create(
            user=request.user, 
            movie=movie, 
            purchase_type=purchase_type, 
            quantity=quantity, 
            price_per_ticket=price, 
            session_time=session_time
            )
        return redirect('users:dashboard_purchases')