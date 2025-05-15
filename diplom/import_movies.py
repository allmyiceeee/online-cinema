import csv
from first.models import Movie, Genre

def run():
    with open('imdb_top_1000.csv', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for row in reader:
            try:
                title = row['Series_Title'].strip()
                # 1. Создаём или находим фильм (по title)
                movie, created = Movie.objects.get_or_create(
                    title=title,
                    defaults={
                        'overview': row['Overview'],
                        'imdb_rating': float(row['IMDB_Rating']),
                        'year': int(row['Released_Year']),
                        'poster_url': row['Poster_Link'],
                        'trailer_id': '',  # если нет трейлера — ставим пустую строку
                    }
                )

                # 2. Разбираем жанры
                genres = [g.strip() for g in row['Genre'].split(',')]
                for genre_name in genres:
                    genre_obj, _ = Genre.objects.get_or_create(genre=genre_name)
                    movie.genre.add(genre_obj)

            except Exception as e:
                print(f"Ошибка при фильме '{row.get('Series_Title')}': {e}")
run()