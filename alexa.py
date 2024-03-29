import speech_recognition as sr
import pyttsx3
import pywhatkit
import wikipedia
import datetime
import keyboard
from pygame import mixer
from colores import capture 
import subprocess as sub
import os



name = "Alexa"
listener = sr.Recognizer()
engine = pyttsx3.init()

voices = engine.getProperty("voices")
engine.setProperty("voices", voices[0].id)



sites = {"opera":"opera.com",
         "youtube":"youtube.com",
         "facebook":"facebook.com",
         "whatsapp":"whatsapp.com",
         "universidad":"https://lamb-academic.upeu.edu.pe/student-portal/pages/student-courses-v2"
         }
programs = {
    "steam":r"C:\Program Files (x86)\Steam\steam.exe",
    "spotify":r"C:\Program Files\WindowsApps\SpotifyAB.SpotifyMusic_1.232.997.0_x64__zpdnekdrzrea0\Spotify.exe",
    "word":r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE"
}
files = {

}
def talk(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("Escuchando...")
        listener.adjust_for_ambient_noise(source)
        pc = listener.listen(source)
    try:
        rec = listener.recognize_google(pc, language="es")
        rec = rec.lower()
        return rec
    except sr.UnknownValueError:
        talk("No te entendí, intenta de nuevo")
        print("No te entendí, intenta de nuevo")
        return ""
    except Exception as e:
        print("Se produjo un error:", e) 
        return ""

def run_Alexa():
    talk("En que puedo ayudarte hoy")
    while True:

        try:
            rec = listen()
        except UnboundLocalError:
            talk("No te entendí, intenta de nuevo")
            print("No te entendí, intenta de nuevo")
            continue     
        if 'reproduce' in rec:
            music = rec.replace('reproduce', '')
            print("Reproduciendo " + music)
            talk("Reproduciendo " + music)
            pywhatkit.playonyt(music)
            talk("necesitas algo mas ?")

        elif "busca" in rec:    
            search = rec.replace("busca","")
            wikipedia.set_lang("es")
            wiki = wikipedia.summary(search, 1)
            print(search + ": "+wiki)
            talk(wiki)
            talk("necesitas algo mas ?")

        elif "alarma" in rec:
            num = rec.replace("alarma ","")
            num = num.strip()
            talk ("alarma "+ num )
            while True:
                if datetime.datetime.now().strftime("%H:%M") == num:
                    print("HORA DE DESPERTAR")
                    while True:
                        mixer.init()
                        mixer.music.load("alarma.mp3")
                        mixer.music.play()
                        while mixer.music.get_busy():
                            if keyboard.read_key() in ["s", "S"]:
                                mixer.music.stop()           
                                break
                        break
                    break
            talk("necesitas algo mas ?")    

        elif "colores" in rec:
            talk("enseguida")
            capture()  
            talk("necesitas algo mas ?")     

        elif "abre" in rec: 
            for site in sites:
                if site in rec:
                    sub.call(f"start opera.exe {sites[site]}",shell=True)
                    talk(f"He abierto {site}")
            talk("necesitas algo mas ?")
            for app in programs:
                if app in rec:
                    talk("abriendo"+ app)
                    os.startfile(programs[app])
                    talk("necesitas algo mas ?")

        elif "archivo" in rec:  
            talk("que archivo buscas?")          
            for file in files:
                if file in rec:
                    sub.Popen([files[file]], shell=True)
                    talk(f"Abriendo {file}")
            talk("necesitas algo mas ?")



        elif "escribe" in rec :
            try:
                with open("nota.txt", "a") as f:
                    write(f)
            except FileNotFoundError as e:
                file = open("nota.txt"  , "w")
                write(file)
            talk("necesitas algo mas ?")

        else:
            "termina" in rec
            talk("apagando sistema")
            break


def write(f):
    talk("que quieres que escriba?")
    rec_escribe = listen()
    f.write(rec_escribe + os.linesep)
    f.close()
    talk("listo , ya puedes revisarlo")
    sub.Popen("nota.txt" , shell=True)

    
                
if __name__ == "__main__":  
    run_Alexa()
