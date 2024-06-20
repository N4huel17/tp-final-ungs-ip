# Introducción a la Programación - primer semestre del 2024.

## Trabajo práctico: galería de imágenes de la NASA 🚀

##INTEGRANTES:
-DIEGO UGARTE
-NAHUEL MENDEZ
-VALENTIN ROMANO

### SINTESIS DEL PROYECTO

- El trabajo consiste en implementar una aplicación web _fullstack_ usando Django Framework, que permita consultar las imágenes de la API pública que proporciona la NASA. La información que provenga de esta API será renderizada por el _framework_ en distintas _cards_ que mostrarán -como mínimo- la imagen en cuestión, un título y una descripción. Adicionalmente -y para enriquecerla- se prevee que los estudiantes desarrollen la lógica necesaria para hacer funcionar el buscador central y un módulo de autenticación básica (usuario/contraseña) para almacenar uno o más resultados como **favoritos**, que luego podrán ser consultados por el usuario al loguearse. En este último, la app deberá tener la lógica suficiente para verificar cuándo una imagen fue marcada en favoritos.

### Extenciones recomendadas : 
After Dark.
Prettier - Code formatter.
Pylance.
Python.
Python Debugger.

## GUIA DE INSTALACION PARA EL PROYECTO 
1) Django (pip install django==4.2.10 ) 
2) pip install -r requirements.txt (dependencias)
3) python manage.py runserver 3000 (comando para levantar el proyecto) 
4) http://localhost:3000 (poner esa url en el navegador)
5)  https://sqlitebrowser.org/dl/ (descargar )


### Metodologia de trabajo: 
trabajo de ramas, cada integrante tendra su rama donde debera trabajar en sus tareas.
1) Rama principal: (Main o master/ dependiendo de la configuracion de la pc )
2) rama de cada integrante
diego01
valentin01
nahuel01
3) comandos : 
git pull (bajar cambios )
git add . (guardar cambios hechos )
git commit -m"mensaje describiendo lo realizado "
git push origin nombreDelaRama (diego01,valen01,nahuel01) = Subir cambios

IMPORTANTE: Antes de empezar a realizar tareas deberan hacer "git pull" en main y bajar los cambios para evitar confictos, luego deberan moverse a sus ramas (git checkout nombre_de_la_rama), seguido una vez estando en su rama poner el comando "git merge main", para traer los cambios de main a sus rama .NUNCA MERGEAR UNA RAMA ESTANDO PARADO EN MAIN

Metodologia Agil: 
SCRUM = Sofware Taiga (repartición de tareas e informes). 

Explicación Funcionalidades Implementadas :
-Nahuel (mostrar las fotos desde la API de la NASA).
Cambios en views.py: Importación Directa de la Función getAllImages:  desde services_nasa_image_gallery.py.
Uso de getAllImages en home: En la función home, llama a getAllImages() para obtener todas las imágenes desde la API de NASA.
Pasaje de Imágenes : Las imágenes obtenidas se pasan como contexto al template 'home.html', donde serán renderizadas.

Cambios en services_nasa_image_gallery.py:
Uso de getAllImages desde transport.py: Importamos y llamamos directamente la función getAllImages desde transport.py para obtener los datos JSON de la API de NASA.
Mapeo a Objetos NASACard: Utilizamos el mapeador fromRequestIntoNASACard para convertir cada objeto JSON en un objeto NASACard.
Retorno de Imágenes Mapeadas: Finalmente, retornamos la lista de imágenes convertidas en objetos NASACard.

-Nahuel (Hacer que el buscador funcione):
Archivo views.py:
Función search(request): Se modificó para manejar tanto la búsqueda como el caso donde no se ingresa ningún término devolver por defecto "space".

*Se utilizó el método POST del formulario para obtener el término de búsqueda (search_msg).
*Se llamó a services_nasa_image_gallery.getAllImages() con el término de búsqueda para obtener las imágenes filtradas.
*Si no se proporcionó un término de búsqueda, se llamó a services_nasa_image_gallery.getAllImages() sin parámetros, lo que devuelve las imágenes relacionadas con "SPACE".

Valentin:
cambios en header.html 
se cambiaron las redirecciones para que al apretar en iniciar sesion te mande a /login y al salir la redireccion sea exit

cambios en view.py
se implementaron las funciones login y authenticate donde la funcion
authenticate verifica las credenciales del usuario(nombre y contraseña)
con los usuarios que se registraron en sistema. Si las credenciales son correctas,
inicia sesion. la funcion login inicia una sesión para el usuario que está autenticado en el sistema,
lo que permite al usuario permanecer autenticado para gestionar alguna accion en la pagina
se crearon la funcion login_view:
Maneja la lógica de autenticación de los usuarios. Verifica que los valores proporcionadas por el usuario y
si son correctas inicia sesión al usuario y lo redirige a la página principal. Si las credenciales 
no son correctas, salta error
logout_view:
Cierra la sesión del usuario y lo redirige a la página de inicio
getAllFavouritesByUser:
renderiza la página de favoritos del usuario
saveFavourite:
agrega un elemento a la lista de favoritos del usuario
deleteFavourite:
 elimina un elemento de la lista de favoritos del usuario





