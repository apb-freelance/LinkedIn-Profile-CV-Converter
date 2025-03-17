import sys
import os
from bs4 import BeautifulSoup
from lib.linkedin.html_text_parser import *

def leer_html(ruta):
    if not os.path.exists(ruta):
        print(f"Error: El archivo '{ruta}' no existe.")
        return
    
    try:
        with open(ruta, 'r', encoding='utf-8') as file:
            contenido = file.read()
            #print("Contenido del archivo HTML cargado correctamente.")
            return contenido
    except Exception as e:
        print(f"Error al leer el archivo: {e}")

def append_to_file(filename, content):
    """Añade contenido a un archivo sin sobrescribirlo."""
    with open(filename, "a", encoding="utf-8") as f:
        f.write(content + "\n")  # Agrega un salto de línea opcional

def get_linkedin_section_about(html_source=""):
    soup = BeautifulSoup(html_source, "html.parser")
    section_html = soup.select_one('section > div > div > div > div > span.visually-hidden')
    excluir_tags = {
        'aria-hidden': ["true"]
    }
    return [section_html, excluir_tags]

def get_linkedin_schema_about(html_section=[]):
    if len(html_section) == 2:
        return generar_esquema_jerarquico(html_section[0], html_section[1])
    else:
        return []

def get_linkedin_section_experience(html_source=""):
    soup = BeautifulSoup(html_source, "html.parser")
    section_html = soup.select_one('main > section')
    excluir_tags = {
        'aria-hidden': ["true"]
    }
    return [section_html, excluir_tags]

def get_linkedin_schema_experience(html_section=[]):
    if len(html_section) == 2:
        return generar_esquema_jerarquico(html_section[0], html_section[1])
    else:
        return []

def get_linkedin_section_projects(html_source=""):
    soup = BeautifulSoup(html_source, "html.parser")
    section_html = soup.select_one('main > section')
    excluir_tags = {
        'aria-hidden': ["true"]
    }
    return [section_html, excluir_tags]

def get_linkedin_schema_projects(html_section=[]):
    if len(html_section) == 2:
        return generar_esquema_jerarquico(html_section[0], html_section[1])
    else:
        return []

def get_linkedin_section_education(html_source=""):
    soup = BeautifulSoup(html_source, "html.parser")
    section_html = soup.select_one('main > section')
    excluir_tags = {
        'aria-hidden': ["true"]
    }
    return [section_html, excluir_tags]

def get_linkedin_schema_education(html_section=[]):
    if len(html_section) == 2:
        return generar_esquema_jerarquico(html_section[0], html_section[1])
    else:
        return []

def get_linkedin_section_skills(html_source=""):
    soup = BeautifulSoup(html_source, "html.parser")
    section_html = soup.select_one('main > section')
    excluir_tags = {
        'aria-hidden': ["true"]
    }
    return [section_html, excluir_tags]

def get_linkedin_schema_skills(html_section=[]):
    if len(html_section) == 2:
        return generar_esquema_jerarquico(html_section[0], html_section[1])
    else:
        return []

def get_linkedin_section_contact(html_source=""):
    soup = BeautifulSoup(html_source, "html.parser")
   # Usando rutas absolutas para encontrar la información
    dialog = soup.select_one('div[aria-labelledby^="pv-contact-info"]')
    return [dialog, None]

def get_linkedin_schema_contact(html_section=[]):
    contact_info = {}
    if len(html_section) == 2:
        dialog = html_section[0]
        contact_list = dialog.select('section.pv-contact-info__contact-type')
        contact_info["Nombre"] = dialog.select_one('h1[id="pv-contact-info"]').get_text(strip=True)
        for value in contact_list:
            k = value.select_one('h3')
            if k:
                k = k.get_text(strip=True)
                v = value.select('div span, div a, ul li a|span, ul li span|span')
                if isinstance(v, list) and len(v) == 1:
                    v = v[0].get_text(strip=True)
                    contact_info[k] = v
                elif isinstance(v, list) and len(v) > 1:
                    contact_info[k] = f"{v[0].get_text(strip=True)} {v[1].get_text(strip=True)}"
    return contact_info