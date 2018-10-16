import speech_recognition as sr
import pygame
import peewee as pw
import googlemaps
import json


gmaps = googlemaps.Client(key = 'AIzaSyCbbzGbkEBCF1nkGRpcGTFgeqhq0LTYu6o')


#print(gmaps.geolocate())
#Clase Base de la Conexión
class BaseModel(pw.Model):
    class Meta:
        myConnection = pw.MySQLDatabase("routes_city", host="127.0.0.1", user = "root", passwd = "")
        myConnection.connect()
        database = myConnection


#Clase Ruta
class route(BaseModel):
    idroute = pw.AutoField()
    name = pw.TextField()

#Clase Bus
class bus(BaseModel):
    idbus = pw.AutoField()
    license_plate = pw.TextField()
    route = pw.ForeignKeyField(route)
    latitude = pw.FloatField()
    longitude = pw.FloatField()

#Clase Palabras Clave
class keywords(BaseModel):
    idkeywords = pw.AutoField()
    keyword = pw.TextField()

#Clase Puntos de Ruta
class points_route(BaseModel):
    idpoints_route = pw.AutoField()
    latitude = pw.FloatField()
    longitude = pw.FloatField()
    route = pw.ForeignKeyField(route)

#Clase Palabras clave de Rutas
class route_keywords(BaseModel):
    idroute_keywords = pw.AutoField()
    route = pw.ForeignKeyField(route)
    keywords = pw.ForeignKeyField(keywords)

'''for keyw in keywords.select():
    print (keyw.idkeywords, keyw.keyword)

for pr in points_route.select():
    print(pr.latitude, pr.longitude, pr.route.name)

print("Rutas que pasan por UTP")
for rt in route_keywords.filter(keywords = keywords.filter(keyword = 'UTP')):
    print(rt.route.name)'''

'''Muestra los puntos de quiebre de ruta centralizados'''
coord = list()
for x in points_route.filter(route = route.filter(name = '3A')):
    print(x.latitude, x.longitude)
    y = list()
    y.append(x.latitude)
    y.append(x.longitude)
    coord.append(y)
data = gmaps.nearest_roads(points = coord)


for x in data:
    print(x['location']['latitude'], x['location']['longitude'])


# obtain audio from the microphone
    
r = sr.Recognizer()
with sr.Microphone(device_index = 0) as source:
    r.adjust_for_ambient_noise(source)
    print("Di alguito!")
    audio = r.listen(source)
print(r.recognize_google(audio))