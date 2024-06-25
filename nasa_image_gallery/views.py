from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from .forms import RegisterForm
from .models import MyUser  # Asegúrate de importar tu modelo personalizado
from .layers.services import services_nasa_image_gallery
from django.contrib.auth.decorators import login_required

def index_page(request):
    return render(request, 'index.html')

def getAllImagesAndFavouriteList(request):
    images = services_nasa_image_gallery.getAllImages()
    favourite_list = []
    if request.user.is_authenticated:
        favourite_list = services_nasa_image_gallery.getAllFavouritesByUser(request)
    return images, favourite_list

def home(request):
    images, favourite_list = getAllImagesAndFavouriteList(request)
    return render(request, 'home.html', {'images': images, 'favourite_list': favourite_list})

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
        return render(request, 'home.html', {'images': images, 'favourite_list': favourite_list})
    else:
        return render(request, 'home.html', {'images': [], 'favourite_list': []})

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
        services_nasa_image_gallery.saveFavourite(request)
    return redirect('home')

@login_required
def deleteFavourite(request):
    if request.method == 'POST':
        services_nasa_image_gallery.deleteFavourite(request)
    return redirect('home')

@login_required
def exit(request):
    pass