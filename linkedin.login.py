from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pickle
import os
import argparse

# Definiendo variables globales
NAME = ""
USERNAME = ""
PASSWORD = ""

# Ingresar credenciales
# Crear el parser de argumentos
parser = argparse.ArgumentParser(description="Script para obtener nombre, usuario y contraseña.")

# Definir los argumentos que se van a pasar
parser.add_argument('--name', type=str, required=True, help="Tu nombre")
parser.add_argument('--username', type=str, required=True, help="Tu nombre de usuario")
parser.add_argument('--password', type=str, required=True, help="Tu contraseña")

# Parsear los argumentos
args = parser.parse_args()

# Asignar los valores de los argumentos a las variables
NAME = args.name
USERNAME = args.username
PASSWORD = args.password

print(f"NAME={NAME}")
print(f"USERNAME={USERNAME}")
print(f"PASSWORD={PASSWORD}")

# Configuración del driver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")  # Maximizar ventana
driver = webdriver.Chrome(options=chrome_options)

# Ruta donde se guardarán las cookies
COOKIE_FILE = "linkedin_cookies.pkl"

# Crear carpeta para guardar los HTML
HTML_FOLDER = "html_data"
os.makedirs(HTML_FOLDER, exist_ok=True)

# URL de LinkedIn
driver.get("https://www.linkedin.com/")
time.sleep(2)  # Espera para cargar la página

# Cargar cookies si existen
if os.path.exists(COOKIE_FILE):
    with open(COOKIE_FILE, "rb") as file:
        cookies = pickle.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)
    driver.refresh()
    time.sleep(2)

# Verificar si ya estamos logueados
if "feed" not in driver.current_url:
    driver.get("https://www.linkedin.com/login")
    time.sleep(2)
    
    # Encontrar campos de usuario y contraseña
    username = driver.find_element(By.ID, "username")
    password = driver.find_element(By.ID, "password")

    username.send_keys(USERNAME)
    password.send_keys(PASSWORD)
    password.send_keys(Keys.RETURN)

    time.sleep(5)  # Esperar a que cargue la página principal
    
    # Guardar cookies después del inicio de sesión
    with open(COOKIE_FILE, "wb") as file:
        pickle.dump(driver.get_cookies(), file)

# Verificar que la sesión se inició correctamente
if "feed" in driver.current_url:
    print("✅ Inicio de sesión exitoso")
    driver.get(f"https://linkedin.com/in/{NAME}")
    time.sleep(3)

    # Definir las secciones del perfil
    secciones = {
        "about": f"https://www.linkedin.com/in/{NAME}/details/about/",
        "experience": f"https://www.linkedin.com/in/{NAME}/details/experience/",
        "education": f"https://www.linkedin.com/in/{NAME}/details/education/",
        "projects": f"https://www.linkedin.com/in/{NAME}/details/projects/",
        "skills": f"https://www.linkedin.com/in/{NAME}/details/skills/",
        "recommendations": f"https://www.linkedin.com/in/{NAME}/details/recommendations/",
        "contact": f"https://www.linkedin.com/in/{NAME}/overlay/contact-info/"
    }
    
    # Descargar cada sección y guardarla en un archivo HTML dentro de la carpeta
    for section, url in secciones.items():
        driver.get(url)
        time.sleep(3)
        with open(os.path.join(HTML_FOLDER, f"linkedin_{section}.html"), "w", encoding="utf-8") as file:
            file.write(driver.page_source)
        print(f"📄 Sección {section} guardada en {HTML_FOLDER}/")
else:
    print("❌ Error en el inicio de sesión")

# Cerrar el navegador sin eliminar las cookies
driver.quit()
# driver.quit()
