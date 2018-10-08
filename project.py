import speech_recognition as sr

# obtain audio from the microphone

'''miclist=sr.Microphone.list_microphone_names()
for x in miclist:
    print(x)'''
    
r = sr.Recognizer()
with sr.Microphone(device_index = 0) as source:
    r.adjust_for_ambient_noise(source)
    print("Say something!")
    audio = r.listen(source)
print(r.recognize_google(audio))