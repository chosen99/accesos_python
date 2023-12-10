import pyttsx3


s = pyttsx3.init()
voz = s.getProperty('voices')
s.setProperty('voice', voz[0].id)
s.setProperty('rate', 130)
data = "Karla Fernanda, Grupo ARBM"
s.say(data)
s.runAndWait()
