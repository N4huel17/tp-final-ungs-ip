# views.py

from django.core.paginator import Paginator
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from .forms import RegisterForm
from .models import MyUser
from .models import Favourite
from .models import NotInterestingImage
from django.http import JsonResponse
from .layers.services import services_nasa_image_gallery
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.utils.translation import activate
from django.utils import translation
import json
import os

# Ruta al archivo JSON de traducciones
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRADUCCIONES_JSON_PATH = os.path.join(BASE_DIR, 'traducciones.json')

# Cargar el diccionario de traducciones desde el archivo JSON
with open(TRADUCCIONES_JSON_PATH, 'r', encoding='utf-8') as file:
    traducciones = json.load(file)


def traducir_palabra(palabra):
    # Función para traducir una palabra del español al inglés
    return traducciones.get(palabra, palabra)



def index_page(request):
    return render(request, 'index.html')

def getAllImagesAndFavouriteList(request):
    images = services_nasa_image_gallery.getAllImages()
    favourite_list = []
    if request.user.is_authenticated:
        favourite_list = services_nasa_image_gallery.getAllFavouritesByUser(request)
    return images, favourite_list

def home(request):
    images = services_nasa_image_gallery.getAllImages()  # Obtener todas las imágenes desde algún servicio o función

    favourite_list = []
    if request.user.is_authenticated:
        favourite_list = services_nasa_image_gallery.getAllFavouritesByUser(request)

    per_page_options = [4, 6, 8, 10, 12]  # Opciones de cantidad de imágenes por página
    per_page = int(request.GET.get('per_page', 6))  # Obtener el número de imágenes por página seleccionado por el usuario
    
    # Obtener todas las imágenes marcadas como no interesantes por el usuario actual
    not_interesting_images = []
    if request.user.is_authenticated:
        not_interesting_images = NotInterestingImage.objects.filter(user=request.user).values_list('image_url', flat=True)


    filtered_images = [img for img in images if img.image_url not in not_interesting_images]

    paginator = Paginator(filtered_images, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'home.html', {
        'page_obj': page_obj,
        'favourite_list': favourite_list,
        'per_page': per_page,
        'per_page_options': per_page_options  # Pasar las opciones de cantidad por página a la plantilla
    })

def search(request):
    if request.method == 'POST':
        search_msg = request.POST.get('query', '').strip()
        if search_msg:
            search_msg = traducir_palabra(search_msg)
            images = services_nasa_image_gallery.getAllImages(search_msg)
        else:
            images = services_nasa_image_gallery.getAllImages()
    else:
        search_msg = request.GET.get('query', '').strip()
        if search_msg:
            images = services_nasa_image_gallery.getAllImages(search_msg)
        else:
            images = services_nasa_image_gallery.getAllImages()

    favourite_list = []
    if request.user.is_authenticated:
        favourite_list = services_nasa_image_gallery.getAllFavouritesByUser(request)

    per_page = int(request.GET.get('per_page', 5))
    per_page_options = [4, 6, 8, 10, 12]

    user = request.user
    not_interesting_images = NotInterestingImage.objects.filter(user=user).values_list('image_url', flat=True)

    filtered_images = [img for img in images if img.image_url not in not_interesting_images]

    paginator = Paginator(filtered_images, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'home.html', {
        'page_obj': page_obj,
        'favourite_list': favourite_list,
        'per_page': per_page,
        'per_page_options': per_page_options,
        'query': search_msg
    })

def change_language(request):
    language = request.GET.get('language', 'es')
    next_url = request.GET.get('next', '/')
    translation.activate(language)
    response = redirect(next_url)
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
    return response

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'registration/login.html', {'error': 'Usuario o contraseña incorrectos'})
    return render(request, 'registration/login.html')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            send_mail(
                'Registro exitoso',
                f'Tus credenciales de acceso:\nUsuario: {user.email}\nContraseña: {form.cleaned_data["password"]}',
                'noreply@yourdomain.com',
                [user.email],
                fail_silently=False,
            )
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('index-page')

@login_required
def getAllFavouritesByUser(request):
    favourite_list = services_nasa_image_gallery.getAllFavouritesByUser(request)
    return render(request, 'favourites.html', {'favourite_list': favourite_list})

@login_required
def saveFavourite(request):
    if request.method == 'POST':
        comment = request.POST.get('comment', '')  # Obtener el comentario del formulario
        favourite, created = Favourite.objects.get_or_create(
            title=request.POST['title'],
            description=request.POST['description'],
            image_url=request.POST['image_url'],
            date=request.POST['date'],
            user=request.user
        )
        if created or favourite.comment != comment:
            favourite.comment = comment
            favourite.save()
     
    return redirect('home')


@login_required
def deleteFavourite(request):
    if request.method == 'POST':
        services_nasa_image_gallery.deleteFavourite(request)
    return redirect('favoritos')

@login_required
def guardar_comentario(request):
    if request.method == 'POST':
        comentario = request.POST.get('comment')
        favorito_id = request.POST.get('id')
        print(f"Comentario recibido: {comentario}")
        print(f"ID del favorito: {favorito_id}")
        
        favorito = get_object_or_404(Favourite, id=favorito_id, user=request.user)
        print(f"Favorito encontrado: {favorito}")
        
        favorito.comment = comentario
        favorito.save()
        print("Comentario guardado.")
        
        return redirect('favoritos')
    else:
        print("Método no permitido.")
        return redirect('favoritos')

@login_required
def exit(request):
    pass


def mark_not_interesting(request):
    if request.method == 'POST':
        image_url = request.POST.get('image_url')
        user = request.user
        NotInterestingImage.objects.get_or_create(image_url=image_url, user=user)

    return redirect('home')