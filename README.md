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
trabajo de ramas, cada integrante tendra su rama donde deberar trabajar en sus tareas
1) Rama principal: (Main o master/ dependiendo de la configuracion de la pc )
2) rama de cada integrante
diego01
valentin01
nahuel01
3) comandos : 
git pull (bajar cambios )
git add . (guardar cambios hechos )
git commit -m"mensaje describiendo lo realizado "
git push origin nombreDelaRama (diego01,valen01,nahuel01)

IMPORTANTE: Antes de empezar a realizar tareas deberan hacer "git pull" en main y bajar los cambios para evitar confictos, luego deberan moverse a sus ramas (git checkout nombre_de_la_rama), seguido una vez estando en su rama poner el comando "git merge main", para traer los cambios de main a sus rama .NUNCA MERGEAR UNA RAMA ESTANDO PARADO EN MAIN
