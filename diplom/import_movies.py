import csv
from first.models import Movie

def run():
    with open('imdb_top_1000.csv', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                Movie.objects.create(
                    title=row.get('Series_Title', '').strip(),
                    genre=row.get('Genre', '').strip(),
                    overview=row.get('Overview', '').strip(),
                    imdb_rating=float(row.get('IMDB_Rating') or 0),
                    year=int(row.get('Released_Year') or 0),
                    poster_url=row.get('Poster_Link', '').strip()
                )
            except Exception as e:
                print(f"Ошибка при импорте строки: {e}")
run()