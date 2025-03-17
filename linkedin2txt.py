import sys
import os
from lib.linkedin.html_parse import *

if __name__ == '__main__':
    # Verificar que se pase un archivo como argumento
    if len(sys.argv) != 2:
        print("Uso: python script.py [path-to-linkedin-section-files]")
        sys.exit(1)

    files = ["contact", "about", "experience", "education", "projects", "skills"]

    # Verificar si el archivo existe y devolver su contenido
    for file in files:
        data = leer_html(f"{sys.argv[1]}/linkedin_{file}.html")
        content = ""

        match file:
            case "contact":
                content = get_linkedin_schema_contact(get_linkedin_section_contact(data))
                content = texto_esquema_v2(content)
            case "about":
                content = get_linkedin_schema_about(get_linkedin_section_about(data))
                content = texto_esquema(content)
            case "skills":
                content = get_linkedin_schema_skills(get_linkedin_section_skills(data))
                content = texto_esquema(content)
            case "experience":
                content = get_linkedin_schema_experience(get_linkedin_section_experience(data))
                content = texto_esquema(content)
            case "education":
                content = get_linkedin_schema_education(get_linkedin_section_education(data))
                content = texto_esquema(content)
            case "projects":
                content = get_linkedin_schema_projects(get_linkedin_section_projects(data))
                content = texto_esquema(content)

        content += "\n" + "-" * 80
        append_to_file("cv.txt", content)

