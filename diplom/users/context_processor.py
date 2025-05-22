def get_menu(request):
    menu = [
        {'title': "Главная страница", 'url_name': 'movie_list'},
        {'title': "О сайте", 'url_name': 'about'},
        {'title': "Обратная связь", 'url_name': 'contact'},     
    ]
    return {'mainmenu': menu}