import speech_recognition as sr
import pygame
import peewee as pw

myConnection = pw.MySQLDatabase("routes_city", host="127.0.0.1", user = "root", passwd = "")

myConnection.connect()

# obtain audio from the microphone
    
r = sr.Recognizer()
with sr.Microphone(device_index = 0) as source:
    r.adjust_for_ambient_noise(source)
    print("Di alguito!")
    audio = r.listen(source)
print(r.recognize_google(audio))