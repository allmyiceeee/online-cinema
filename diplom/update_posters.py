import os
import django
import requests

# Настройка Django окружения
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diplom.settings')
django.setup()

from first.models import Movie 

API_KEY = '4aaa2e5c484bf9dea5ab38738d634d7f'  
TMDB_SEARCH_URL = 'https://api.themoviedb.org/3/search/movie'
TMDB_IMAGE_BASE_URL = 'https://image.tmdb.org/t/p/w500'

def get_poster_url(title):
    params = {
        'api_key': API_KEY,
        'query': title,
        'include_adult': False
    }
    proxies = {
        "http": "http://HwT9NfWn:SJ3NkVWb@185.101.202.17:64998",
        "https": "http://HwT9NfWn:SJ3NkVWb@185.101.202.17:64998"
    }
    response = requests.get(TMDB_SEARCH_URL, params=params, proxies=proxies)
    if response.status_code == 200:
        data = response.json()
        print(f"Ответ для '{title}':", data)
        if data['results']:
            poster_path = data['results'][0].get('poster_path')
            if poster_path:
                return f"{TMDB_IMAGE_BASE_URL}{poster_path}"
    return None


def update_movies_with_posters():
    movies = Movie.objects.all()
    for movie in movies:
        poster_url = get_poster_url(movie.title)
        if poster_url:
            movie.poster_url = poster_url
            movie.save()
            print(f"[✓] Обновлено: {movie.title}")
        else:
            print(f"[✗] Постер не найден: {movie.title}")

if __name__ == '__main__':
    update_movies_with_posters()
