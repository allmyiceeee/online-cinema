from django.contrib import admin
from .models import Movie, Feedback
# Register your models here.
class MovieAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    ordering = ['id']
admin.site.register(Movie, MovieAdmin)

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message', 'create_time')