from django.db import models

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)
    overview = models.TextField()
    imdb_rating = models.FloatField()
    year = models.IntegerField()
    poster_url = models.URLField()
    
    def __str__(self):
        return self.title
    
class Feedback(models.Model):
    name = models.CharField('Имя', max_length=100)    
    email = models.EmailField('Email')    
    message = models.TextField('Сообщение')    
    create_time = models.DateTimeField('Дата отправки', auto_now_add=True)    
    
    def __str__(self):
        return f'{self.name} ({self.email}) — {self.created_at:%Y-%m-%d %H:%M}'
