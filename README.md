# Machine Learning Proyecto 2

## Descripcion

En este repositorio podran encontrar el codigo y video de manim ilustrando 3 metodos de clasificacion de machine learning, estos siendo KNN, Arboles de decision y Regresion logistica. Se ha usado de motivacion la aplicacion a identificar un musil de un pajaro en radares.

## Software usado

Se ha usado Python junto con las librerias manim para la creacion del video y numpy para graficar.

## Como construir y compilar

Este codigo esta compuesto de 7 escenas. La primera seria la introduccion en la que se presenta el titulo. La segunda escena es la presentacion del radar en la que se muestra el mismo y con animaciones se muestra la aparicion de los puntos de misiles y pajaros con su respectivo color y tamaño para diferenciar. La tercera escena muestra los datos del radar pero en un plano cartersiano. La cuarta esena es la explicacion grafica de la aplicacion del metodo de K-Nearest Neighbor (KNN), en el que se simula un nuevo dato a clasificar para saber si sera identificado como misil o pajaro, este dependiendo de los puntos mas cercanos a este. En la quinta escena sobre arboles de decision en el que se define las dimensiones que definiran las clasificacion de los puntos. En la sexta escena esta la simulacion del metodo de regresion lineal. En la septima y ultima escena tenemos la matriz de confusion y los resultados de precision.

Para compilar el video en formato mp4 se usa el siguiente comando "manim -pql {nombre del archivo.py} {Nombre de la funcion de scene}":
- manim -pql proyecto2_clasificacion.py ClasificacionDefensa

Y en formato MPEG (.mpg) se puede obtener usando FFmpeg de la siguiente manera:
- ffmpeg -i "C:\Ruta\Al\Proyecto\videos\clasificacion\ClasificacionDefensa.mp4
- c:v mpeg2video -qscale:v 2
