from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Wishlist(models.Model):
    wishlist_type_choises = [
        ('home', 'Смотреть дома'),
        ('cinema', 'Смотреть в кино'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey('first.Movie', on_delete=models.CASCADE)
    wishlist_type = models.CharField(max_length=20, choices=wishlist_type_choises)
    creared_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'movie', 'wishlist_type')
        
class Rating(models.Model):
    rating_choices = [
        (1, 'Нравится'),
        (2, 'Не нравится'),
    ]
    
    movie = models.ForeignKey('first.Movie', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=rating_choices)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('movie', 'user')
        
class WatchedMovie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey('first.Movie', on_delete=models.CASCADE)
    watched_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'movie')
        
class Purchase(models.Model):
    PURCHASE_TYPE_CHOICES = [
        ('home', 'Просмотр дома'),
        ('cinema', 'Поход в кинотеатр'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey('first.Movie', on_delete=models.CASCADE)
    purchase_type = models.CharField(max_length=10, choices=PURCHASE_TYPE_CHOICES)
    quantity = models.PositiveIntegerField(default=1)
    price_per_ticket = models.DecimalField(max_digits=6, decimal_places=2)
    purchased_at = models.DateTimeField(auto_now_add=True)
    session_time = models.DateTimeField(null=True, blank=True)  # Только для кино

    def total_price(self):
        return self.quantity * self.price_per_ticket

    class Meta:
        ordering = ['-purchased_at']
