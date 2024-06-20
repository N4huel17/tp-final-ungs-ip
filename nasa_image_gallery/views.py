
# capa de vista/presentación
# si se necesita algún dato (lista, valor, etc), esta capa SIEMPRE se comunica con services_nasa_image_gallery.py

from django.shortcuts import redirect, render
from .layers.services import services_nasa_image_gallery
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login

# función que invoca al template del índice de la aplicación.
def index_page(request):
    return render(request, 'index.html')

# auxiliar: retorna 2 listados -> uno de las imágenes de la API y otro de los favoritos del usuario.
def getAllImagesAndFavouriteList(request):
    images = services_nasa_image_gallery.getAllImages()
    favourite_list = []
    if request.user.is_authenticated:
        favourite_list = services_nasa_image_gallery.getAllFavouritesByUser(request)

    return images, favourite_list

# función principal de la galería.
def home(request):
    # llama a la función auxiliar getAllImagesAndFavouriteList() y obtiene 2 listados: uno de las imágenes de la API y otro de favoritos por usuario*.
    # (*) este último, solo si se desarrolló el opcional de favoritos; caso contrario, será un listado vacío [].
    images, favourite_list = getAllImagesAndFavouriteList(request)

    return render(request, 'home.html', {'images': images, 'favourite_list': favourite_list} )


# función utilizada en el buscador.
def search(request):
    if request.method== 'POST':
        search_msg = request.POST.get('query', '').strip()
        if search_msg:
            images= services_nasa_image_gallery.getAllImages(search_msg)
        else:
            images=services_nasa_image_gallery.getAllImages()
        favourite_list=[]
        if request.user.is_authenticated:
            favourite_list=  services_nasa_image_gallery.getAllFavouritesByUser(request)
        return render(request, 'home.html', {'images': images, 'favourite_list': favourite_list})


    else:
          return render(request, 'home.html', {'images': [], 'favourite_list': []})

    # si el usuario no ingresó texto alguno, debe refrescar la página; caso contrario, debe filtrar aquellas imágenes que posean el texto de búsqueda.
    pass

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']


        user = authenticate(username=username, password=password)   #Utiliza la función implementada #authenticate para verificar al usuario.
        if user is not None:
            login(request, user)  # Esto establece la sesion del usuario
            return redirect('home')
        else:
            return render(request, 'registration/login.html', {'error': 'Usuario o contraseña incorrectos'})
    return render(request, 'registration/login.html')




@login_required
def logout_view(request):
    logout(request)
    return redirect('index-page')

# las siguientes funciones se utilizan para agregar favoritos: traen los favoritos de un usuario los guarda y elimina 
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