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