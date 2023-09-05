import speech_recognition as sr
import pyttsx3
import pywhatkit

name = "jarvis"
listener = sr.Recognizer()
engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def talk(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    rec = ""
    try:
        with sr.Microphone() as source:
            print("Escuchando...")
            
            # Ajustar para el ruido de fondo
            listener.adjust_for_ambient_noise(source)
            
            audio = listener.listen(source)
            rec = listener.recognize_google(audio, language="es-ES")
            
            # Imprimir el texto reconocido para depuración
            print("Texto reconocido:", rec)
            
            rec = rec.lower()
            
            if name in rec:
                rec = rec.replace(name, '')
    except sr.UnknownValueError:
        print("No se pudo entender el comando de voz")
    except sr.RequestError as e:
        print(f"Error al realizar la solicitud de reconocimiento de voz: {str(e)}")
    
    return rec

def run_jarvis():
    rec = listen()
    
    if rec:
        if 'reproduce ' in rec:
            music = rec.replace('reproduce', '')
            print("Reproduciendo" + music)
            talk("Reproduciendo" + music)
            pywhatkit.playonyt(music)
        else:
            print("Comando no reconocido")

if __name__ == '__main__':
    run_jarvis()
