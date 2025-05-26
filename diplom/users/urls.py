
from django.contrib import admin
from django.urls import path
from . import views
app_name = 'users'

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('profile/', views.profile, name='profile'),
    path('dashboard_wishlist/wishlist/<str:type>/', views.wishlist_view, name='dashboard_wishlist'),
    path('movie/<int:movie_id>/wishlist/', views.add_to_wishlist, name='add_to_wishlist'),
    path('watched/add/<int:movie_id>/', views.add_to_watched, name='add_to_watched'),
    path('watched/', views.watched_movies_view, name='dashboard_watched'),
    path('rate/<int:movie_id>/<str:value>/', views.rate_movie, name='rate_movie'),
    path('rated/', views.rated_movies_view, name='dashboard_rated'),
    path('purchases/', views.purchase_history, name='dashboard_purchases'),
    path('buy/<int:movie_id>/', views.buy_ticket, name='buy_ticket'),
]
