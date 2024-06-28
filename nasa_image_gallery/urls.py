
from django.contrib import admin
from django.urls import path, include 
from . import views
from django.conf.urls.i18n import i18n_patterns




urlpatterns = [
    path('', views.index_page, name='index-page'),
    path('login/', views.login_view, name='login'),
    path('home/', views.home, name='home'),
    path('buscar/', views.search, name='buscar'),
    path('favourites/', views.getAllFavouritesByUser, name='favoritos'),
    path('favourites/add/', views.saveFavourite, name='agregar-favorito'),
    path('favourites/delete/', views.deleteFavourite, name='borrar-favorito'),
    path('favourites/guardar_comentario/', views.guardar_comentario, name='guardar_comentario'), 
    path('marcar-no-interesante/', views.mark_not_interesting, name='marcar-no-interesante'),
    path('exit/', views.logout_view, name='exit'),
    path('register/', views.register_view, name='register'),
    
    path('exit/', views.logout_view, name='exit'),
    path('register/', views.register_view, name='register'),
    path('change-language/', views.change_language, name='change_language'),
    path('i18n/', include('django.conf.urls.i18n')),
]