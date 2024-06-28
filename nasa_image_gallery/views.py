# views.py

from django.core.paginator import Paginator
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from .forms import RegisterForm
from .models import MyUser
from .models import Favourite
from .layers.services import services_nasa_image_gallery
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.utils.translation import activate




def index_page(request):
    return render(request, 'index.html')

def getAllImagesAndFavouriteList(request):
    images = services_nasa_image_gallery.getAllImages()
    favourite_list = []
    if request.user.is_authenticated:
        favourite_list = services_nasa_image_gallery.getAllFavouritesByUser(request)
    return images, favourite_list


def home(request):
    images = services_nasa_image_gallery.getAllImages()  # Obtener todas las imágenes
    favourite_list = services_nasa_image_gallery.getAllFavouritesByUser(request)
    
    per_page_options = [4, 6, 8, 10, 12]  # Opciones de cantidad de imágenes por página
    per_page = int(request.GET.get('per_page', 6))  # Obtener el número de imágenes por página seleccionado por el usuario
    
    paginator = Paginator(images, per_page)
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
            images = services_nasa_image_gallery.getAllImages(search_msg)
        else:
            images = services_nasa_image_gallery.getAllImages()
        favourite_list = []
        if request.user.is_authenticated:
            favourite_list = services_nasa_image_gallery.getAllFavouritesByUser(request)
        per_page = int(request.GET.get('per_page', 5))
        paginator = Paginator(images, per_page)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'home.html', {'page_obj': page_obj, 'favourite_list': favourite_list, 'per_page': per_page})
    else:
        return render(request, 'home.html', {'images': [], 'favourite_list': []})
    
    
def change_language(request):
    if request.method == 'GET' and 'language' in request.GET:
        language = request.GET['language']
        activate(language)
        next_page = request.GET.get('next', '/')
        print(f'Idioma activado: {language}')
        print(f'Redirigiendo a: {next_page}')
    
    # Redirige de vuelta a la página actual después de cambiar el idioma
    next_page = request.GET.get('next', '/')
    return redirect(next_page)

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
    return redirect('home')

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