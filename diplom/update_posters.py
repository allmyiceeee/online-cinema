import os
import django


# Настройка Django окружения
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diplom.settings')
django.setup()

import requests
from first.models import Movie 

API_KEY = ''  
TMDB_SEARCH_URL = 'https://api.themoviedb.org/3/search/movie'
TMDB_IMAGE_BASE_URL = 'https://image.tmdb.org/t/p/w500'

def get_poster_url(title):
    '''
Получает URL постера для фильма с указанным названием. 
Функция отправляет запрос GET в API TMDB с названием фильма в качестве параметра запроса. Если путь постера не равен None, функция возвращает URL изображения постера, 
объединяя базовый URL изображения TMDB с путем постера.Если код статуса ответа не равен 200 или путь постера равен None, функция возвращает None.
:param title: Название фильма
:return: URL изображения постера или None
'''
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
    '''
    Функция проверяет наличие постеров и обновляет их, если они есть.
    Можно дополнить функцию, чтобы обновляло те постеры, которых нет. Однако это вызывало ошибку, что постеры не обновлялись,
    при первом запуске сайта, постеры снова берутся с сайта, что занимает 10+- минут
    '''
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
