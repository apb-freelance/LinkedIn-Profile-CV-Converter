import sys
from bs4 import BeautifulSoup

def formatear_html(archivo_html):
    """ Lee, analiza y formatea un archivo HTML correctamente indentado. """
    try:
        with open(archivo_html, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')  # Analiza el HTML

        # Formatear con indentación bonita y sin saltos de línea extra
        html_formateado = soup.prettify()

        print(html_formateado)

    except Exception as e:
        print(f"❌ Error al procesar el archivo: {e}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Uso: python formatear_html.py archivo.html")
        sys.exit(1)

    archivo_html = sys.argv[1]
    formatear_html(archivo_html)
