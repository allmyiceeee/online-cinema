from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render  # noqa: F811
from first.models import Movie, Genre
from django.db.models import Prefetch
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from .forms import FeedbackForm
from django.core.paginator import Paginator

menu = [
        {'title': "Главная страница", 'url_name': 'movie_list'},
        {'title': "О сайте", 'url_name': 'about'},
        {'title': "Обратная связь", 'url_name': 'contact'},     
]

# Create your views here.
def index(request: HttpRequest) -> HttpResponse:
    
    date = {
        'title': 'Главная страница',
        'menu': menu
        }
    return render(request, 'first/index.html', context= date)

def about(request: HttpRequest) -> HttpResponse:
    return render(request, 'first/about.html', {'title': 'О сайте', 'menu': menu}) 

def recc(request: HttpRequest) -> HttpResponse:
    return render(request, 'first/recc.html', {'title': 'О сайте', 'menu': menu}) 

def contact(request: HttpRequest) -> HttpResponse:
    '''Если форма валидна сохраняем сообщение в БД и показываем сообщение об успехе'''
    # Создаём форму либо с данными из POST, либо пустую
    form = FeedbackForm(request.POST or None)
    success = False

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            success = True
            # после сохранения сбросим форму, чтобы на странице 
            # отобразилась пустая форма с сообщением об успехе
            form = FeedbackForm()
    return render(request, 'first/contact.html', 
            {
            'title': 'Обратная связь',
            'menu': menu, 
            'form': form, 
            'success': success
            }) 

def login(request: HttpRequest) -> HttpResponse:
    return render(request, 'users/login.html', {'title': 'О сайте', 'menu': menu}) 

#Рекомендательная система

# Загружаем фильмы из базы
def load_movie_data():
    # Загружаем все фильмы с жанрами
    movies = Movie.objects.prefetch_related(
        Prefetch('genre', queryset=Genre.objects.all(), to_attr='genre_list')
    ).all()
    
    movie_data = []
    
    for movie in movies:
        # Получаем список жанров фильма (объединяем их в строку)
        genres = [genre.genre for genre in movie.genre_list]
        combined = ' '.join(genres) + ' ' + movie.overview
        movie_data.append({
            'id': movie.id,
            'title': movie.title,
            'overview': movie.overview,
            'poster_url': movie.poster_url,
            'combined': combined
        })
    
    df = pd.DataFrame(movie_data)
    return df

# Получаем рекомендации
def get_recommendations(movie_id, top_n=5):
    df = load_movie_data()
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['combined'])

    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    indices = pd.Series(df.index, index=df['id'])
    idx = indices[movie_id]

    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n+1]
    movie_indices = [i[0] for i in sim_scores]

    return df.iloc[movie_indices].to_dict(orient='records')

# View: показать рекомендации для одного фильма
def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)

    recommendations = get_recommendations(movie.id)

    return render(request, 'first/movie_detail.html', 
    {
        'movie': movie,
        'recommended_movies': recommendations,
        'menu': menu,
    })
    
    
def movie_list(request):
    selected_id = request.GET.get('category')
    all_genres = Genre.objects.order_by('genre')
    
    if selected_id:
        chosen_genre = get_object_or_404(Genre, pk=selected_id)
        qs = Movie.objects.filter(genre=chosen_genre)
    else:
        chosen_genre=None
        qs = Movie.objects.all()
    query = request.GET.get('q')
    
    if query:
        qs = qs.filter(title__icontains=query)
    qs = qs.order_by('title')
    
    
    paginator = Paginator(qs, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)    
    context = {
        'page_obj': page_obj,
        'all_genres': all_genres,
        'menu': menu,
        'selected_genre': chosen_genre,
        'query': query,
    }
    return render(request, 'first/movie_list.html', context)   