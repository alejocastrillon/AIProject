import speech_recognition as sr
import peewee as pw
import googlemaps
import json
import nltk
from nltk import load_parser
import mysql.connector

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
'''coord = list()
for x in points_route.filter(route = route.filter(name = '3A')):
    print(x.latitude, x.longitude)
    y = list()
    y.append(x.latitude)
    y.append(x.longitude)
    coord.append(y)
data = gmaps.nearest_roads(points = coord)


for x in data:
    print(x['location']['latitude'], x['location']['longitude'])'''


cnx = mysql.connector.connect(user='root', password='',
                              host='127.0.0.1',
                              database='routes_city')

cursor = cnx.cursor()

# obtain audio from the microphone
cp = load_parser('myGrammar/grammar.fcfg')
cs = load_parser('myGrammar/senseQuestion.fcfg')
#nltk.data.show_cfg('/home/alejandro/DocumentosmyGrammar/grammar/fcfg')
    
r = sr.Recognizer()
with sr.Microphone(device_index = 0) as source:
    r.adjust_for_ambient_noise(source)
    print("Di alguito!")
    audio = r.listen(source)
print("Cargando")
try:
    data = (r.recognize_google(audio))
    print(data)
    trees = list(cp.parse(data.split()))
    answer = trees[0].label()['SEM']
    answer = [s for s in answer if s]
    answerSQL = ' '.join(answer)
    treesS = list(cs.parse(data.split()))
    typeQ = treesS[0].label()['SEM']
    typeQ = [s for s in typeQ if s]
    typeQuestion = ' '.join(typeQ)
    print(typeQuestion)
    print(answerSQL)
    cursor.execute(answerSQL)
    for keywords_id in cursor:
        if typeQuestion == 'lugares':
            for x in keywords.filter(idkeywords = keywords_id):
                print(x.keyword)
        elif typeQuestion == 'rutas':
            for x in route.filter(idroute = keywords_id):
                print(x.name)
except sr.UnknownValueError:
    print("Google Speech Recognition no pudo reconocer el audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))