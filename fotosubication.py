# importamos solo la clase Image de la libreria exif, os, folium, gpxpy, que son las que vamos a utilizar 
from exif import Image 
import os
import folium
import gpxpy

# despues de investigar en chatGPT ya se como realizar la extracion de los datos que requiero para mis 5 fotos
# primero definimos convertir_a_decimal y convertimos las coordenadas 
def convertir_a_decimal(coordenadas, ref):
    decimal = coordenadas[0] + coordenadas[1]/60 + coordenadas[2]/3600
    if ref == "S" or ref == "W" : decimal = -decimal
    return decimal
# lectura de la ruta gpx 
# toca iniciar la lista  y  ruta_gpx
ruta_gpx = os.path.join("Datos", "ruta.gpx")
positions = []

# ahora si procedemos con el with
with open(ruta_gpx) as gpx_file:

    myGPX = gpxpy.parse(gpx_file)
    

    for track in myGPX.tracks:
        for segment in track.segments:
            for point in segment.points:
                myPosition = (point.latitude, point.longitude)
                positions.append(myPosition)

#lectura de fotos 
# hacemos una lista con los archivos jpg que vamos a trabajar 
imagenes = ["foto1.JPG", "foto2.JPG", "foto3.JPG", "foto4.JPG", "foto5.JPG"]

#iniciamos la lista vacia de la posición de las fotos 
position_foto = []

imagenes = os.listdir("Datos")

# creamos un cliclo for usando lo que me recomendo chatGPT toca repasar para que es las parte de ruta 
for nombre in imagenes:
    if nombre.lower().endswith(".jpg"):
        # no se para que sirve toca estudiar fijo me lo pregunta 
        ruta = os.path.join("Datos", nombre)
# desoues de definir ruta con lo visto en clase convertimos las imagenes en modo binario
    with open(ruta, "rb") as image_file:
        my_imagen = Image(image_file)

        if my_imagen.has_exif and hasattr(my_imagen, "gps_latitude"):
            
            # se usa hasattr insertar exolicacion de que es y como se come 

            lat = convertir_a_decimal(my_imagen.gps_latitude, my_imagen.gps_latitude_ref)
            lon = convertir_a_decimal(my_imagen.gps_longitude, my_imagen.gps_longitude_ref)
            position_foto.append((lat, lon, nombre))
    
       
# crear mapa 
if positions:
    # crear mapa
    mapa = folium.Map(location=positions[0], zoom_start=13)
    folium.PolyLine(positions, color="red", weight=3, opacity=0.8).add_to(mapa)


# ciclo for para la incorporación de los datos de las fotos al mapa 

    for lat, lon, nombre in position_foto:

        html = f'<img src="Datos/{nombre}" width="200">' 

        folium.Marker(location=[lat, lon], popup=folium.Popup(html, max_width=250), icon=folium.Icon(color="blue", icon="camera", prefix="fa")).add_to(mapa)

mapa.save("mapa_completo.html")
import webbrowser
webbrowser.open("mapa_completo.html")