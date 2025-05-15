from django.db import models

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=255)
    genre = models.ManyToManyField('Genre')
    overview = models.TextField()
    imdb_rating = models.FloatField()
    year = models.IntegerField()
    poster_url = models.URLField()
    trailer_id = models.CharField(max_length=20,blank=True, null=True)
    
    def __str__(self):
        return self.title
    
class Feedback(models.Model):
    name = models.CharField('Имя', max_length=100)    
    email = models.EmailField('Email')    
    message = models.TextField('Сообщение')    
    create_time = models.DateTimeField('Дата отправки', auto_now_add=True)    
    
    def __str__(self):
        return f'{self.name} ({self.email}) — {self.create_time:%Y-%m-%d %H:%M}'

class Genre(models.Model):
    genre = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.genre