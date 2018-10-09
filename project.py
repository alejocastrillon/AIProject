import speech_recognition as sr
import pygame

# obtain audio from the microphone
    
r = sr.Recognizer()
with sr.Microphone(device_index = 0) as source:
    r.adjust_for_ambient_noise(source)
    print("Di alguito!")
    audio = r.listen(source)
print(r.recognize_google(audio))