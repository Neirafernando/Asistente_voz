
from selenium import webdriver
import speech_recognition as sr
import pyttsx3
import pywhatkit

# Ruta del controlador de chrome
chrome_driver_path = 'C:\Users\fernando\Documents\driverchrome\chromedriver'

# Inicializar controlador de Chrome
driver = webdriver.Chrome(executable_path=chrome_driver_path)

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

# Función para interactuar con el navegador
def interactuar_con_navegador(url, xpath_elemento=None, texto_a_ingresar=None):
    # Inicializa el controlador de Chrome
    driver = webdriver.Chrome(executable_path=chrome_driver_path)
    
    try:
        # Abrir la página web especificada
        driver.get(url)
        
        if xpath_elemento:
            # Realizar clic en un elemento si se proporciona una ruta (xpath)
            elemento = driver.find_element_by_xpath(xpath_elemento)
            elemento.click()
        
        if texto_a_ingresar:
            # Ingresar texto en un campo de entrada si se proporciona texto
            campo_texto = driver.find_element_by_id('id_del_campo')  # Reemplaza con el ID correcto
            campo_texto.send_keys(texto_a_ingresar)
        
        # Realizar otras acciones si es necesario
        
    except Exception as e:
        print(f"Error al interactuar con el navegador: {str(e)}")
    finally:
        # Cerrar el navegador al finalizar
        driver.quit()

#Funcion para manipular a traves de comando de voz
def ejecutar_comando_voz(comando):
    if 'abrir página' in comando:
        url = comando.replace('abrir página', '')
        interactuar_con_navegador(url)
    elif 'hacer clic en' in comando:
        elemento = comando.replace('hacer clic en', '')
        interactuar_con_navegador('https://www.ejemplo.com', xpath_elemento=elemento)
    elif 'escribir' in comando:
        texto = comando.replace('escribir', '')
        interactuar_con_navegador('https://www.ejemplo.com', texto_a_ingresar=texto)
    else:
        print("Comando no reconocido")


if __name__ == '__main__':
    run_jarvis()

