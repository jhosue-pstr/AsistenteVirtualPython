import speech_recognition as sr
import pyttsx3
import pywhatkit

name = "Alexa"
listener = sr.Recognizer()
engine = pyttsx3.init()

voices = engine.getProperty("voices")
engine.setProperty("voices", voices[0].id)

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
        print("No te entendí, intenta de nuevo")
        return ""
    except Exception as e:
        print("Se produjo un error:", e) 
        return ""

def run_Alexa():
    while True:
            try:
                rec = listen()
            except UnboundLocalError:
                print("No te entendí, intenta de nuevo")
                continue     
            if 'reproduce' in rec:
                music = rec.replace('reproduce', '')
                print("Reproduciendo " + music)
                talk("Reproduciendo " + music)
                pywhatkit.playonyt(music)
if __name__ == "__main__":  
    run_Alexa()
