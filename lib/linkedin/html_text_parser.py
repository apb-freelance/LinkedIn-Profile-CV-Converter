from bs4 import BeautifulSoup
"""
def organizar_datos(estructura):
    resultado = ""
    
    def procesar_nivel(nivel, prefijo=""): 
        nonlocal resultado
        for item in nivel:
            if isinstance(item, list):
                if isinstance(item[0], list):
                    procesar_nivel(item, prefijo)
                else:
                    clave = item[0][0]
                    valor = item[1][0] if len(item) > 1 else ""
                    resultado += f"{prefijo}- {clave}"
                    if valor:
                        resultado += f" ({valor})"
                    resultado += "\n"
    
    # Procesar la estructura
    procesar_nivel(estructura)
"""

def organizar_datos(estructura):
    resultado = ""
    
    def procesar_nivel(nivel, prefijo=""):
        nonlocal resultado
        
        if isinstance(nivel, dict):  # Manejo de diccionarios
            for clave, valor in nivel.items():
                resultado += f"{prefijo}- {clave}: "
                if isinstance(valor, (dict, list)):  # Si el valor es otro diccionario o lista, procesar recursivamente
                    resultado += "\n"
                    procesar_nivel(valor, prefijo + "  ")
                else:
                    resultado += f"{valor}\n"
        
        elif isinstance(nivel, list):  # Manejo de listas
            for item in nivel:
                if isinstance(item, tuple) and len(item) == 2:  # Manejo de tuplas (clave, valor)
                    clave, valor = item
                    resultado += f"{prefijo}- {clave} ({valor})\n"
                elif isinstance(item, (dict, list)):  # Si el item es un diccionario o lista, procesar recursivamente
                    procesar_nivel(item, prefijo + "  ")
                else:
                    resultado += f"{prefijo}- {item}\n"
    
    # Procesar la estructura
    procesar_nivel(estructura)
    
    return resultado

def organizar_datos_v2(estructura):
    resultado = ""
    
    def procesar_nivel(nivel):
        nonlocal resultado
        
        if isinstance(nivel, dict):  # Manejo de diccionarios
            for clave, valor in nivel.items():
                if isinstance(valor, (dict, list)):  # Si el valor es otro diccionario o lista, procesar recursivamente
                    procesar_nivel(valor)
                else:
                    resultado += f"{clave}: {valor}\n"
        
        elif isinstance(nivel, list):  # Manejo de listas
            for item in nivel:
                if isinstance(item, tuple) and len(item) == 2:  # Manejo de tuplas (clave, valor)
                    clave, valor = item
                    resultado += f"{clave}: {valor}\n"
                elif isinstance(item, (dict, list)):  # Si el item es un diccionario o lista, procesar recursivamente
                    procesar_nivel(item)
                else:
                    resultado += f"{item}\n"
    
    # Procesar la estructura
    procesar_nivel(estructura)
    
    return resultado

def limpiar_estructura(estructura):
    """Elimina listas anidadas innecesarias y normaliza la jerarquía."""
    if isinstance(estructura, list):
        # Eliminar listas anidadas en exceso
        estructura = [limpiar_estructura(e) for e in estructura if e is not None]
        
        # Si la lista tiene solo un elemento que es otra lista, quitar la capa extra
        if len(estructura) == 1 and isinstance(estructura[0], list):
            return estructura[0]

        return estructura
    return estructura

def generar_esquema_jerarquico(elemento, excluir_tags=None):
    """Genera una estructura jerárquica sin exceso de listas anidadas."""
    
    if excluir_tags is None:
        excluir_tags = {}

    def recorrer_elemento(elemento):
        """Recorre el HTML y construye una estructura jerárquica compacta."""
        if elemento.name and any(elemento.get(attr) in valores for attr, valores in excluir_tags.items()):
            return None  # Omitir este elemento y sus hijos si tiene una propiedad excluida

        hijos = []
        for hijo in elemento.children:
            if hijo.name is None:  # Si es texto dentro de un tag
                texto = hijo.strip()
                if texto:
                    hijos.append(texto)
            else:
                sub_esquema = recorrer_elemento(hijo)
                if sub_esquema:
                    hijos.append(sub_esquema)

        if not hijos:
            return None  # Si no hay contenido válido, no devolver nada
        elif len(hijos) == 1 and isinstance(hijos[0], str):
            return tuple(hijos)  # Convertir en tupla si solo hay un texto
        else:
            return hijos  # Mantener como lista solo si hay más de un elemento

    # Generar la estructura base
    estructura = recorrer_elemento(elemento)
    
    # Limpiar listas anidadas innecesarias
    return limpiar_estructura(estructura)

def mostrar_esquema(esquema, nivel=0):
    """Muestra en pantalla la estructura de manera legible."""
    if isinstance(esquema, list):
        for item in esquema:
            mostrar_esquema(item, nivel + 1)
    elif isinstance(esquema, tuple):
        print(" " * nivel + f"- {esquema[0]}")
    else:
        print(" " * nivel + f"- {esquema}")

def texto_esquema(esquema, nivel=0, resultado=None):
    """Almacena la estructura en una variable de texto línea a línea."""
    if resultado is None:
        resultado = []  # Lista para almacenar las líneas
    
    if isinstance(esquema, list):
        for item in esquema:
            texto_esquema(item, nivel + 1, resultado)
    elif isinstance(esquema, tuple):
        resultado.append(" " * nivel + f"- {esquema[0]}")
    else:
        resultado.append(" " * nivel + f"- {esquema}")
    
    return "\n".join(resultado)  # Unir las líneas en una sola cadena

def texto_esquema_v2(esquema, nivel=0, resultado=None):
    """Almacena la estructura en una variable de texto línea a línea con nombre: valor."""
    if resultado is None:
        resultado = []  # Lista para almacenar las líneas
    
    if isinstance(esquema, dict):  # Si es un diccionario
        for clave, valor in esquema.items():
            if isinstance(valor, (dict, list)):  # Si el valor es otro diccionario o lista
                resultado.append(" " * nivel + f"{clave}:")
                texto_esquema(valor, nivel + 1, resultado)  # Procesar recursivamente
            else:
                resultado.append(" " * nivel + f"{clave}: {valor}")
    elif isinstance(esquema, list):  # Si es una lista
        for item in esquema:
            texto_esquema(item, nivel, resultado)  # Procesar recursivamente cada item
    elif isinstance(esquema, tuple) and len(esquema) == 2:  # Si es una tupla (clave, valor)
        resultado.append(" " * nivel + f"{esquema[0]}: {esquema[1]}")
    else:  # En caso de que sea un valor simple
        resultado.append(" " * nivel + f"- {esquema}")
    
    return "\n".join(resultado)  # Unir las líneas en una sola cadena

# # --------------------- EJEMPLO DE USO ---------------------
# html_texto = """
# <div>
#     <h1>Nombre</h1>
#     <p class="omitido">Este texto no debería aparecer</p>
#     <div>
#         <p>Descripción</p>
#         <ul>
#             <li>Trabajo 1</li>
#             <li>Trabajo 2</li>
#         </ul>
#     </div>
# </div>
# """

# # Parsear el HTML y seleccionar un elemento específico
# soup = BeautifulSoup(html_texto, "html.parser")
# elemento_base = soup.find("div")  # Se puede cambiar por otro elemento

# # Definir qué atributos ignorar
# excluir_tags = {
#     "class": ["omitido"],        # Ignorar elementos con class="omitido"
#     "style": ["display:none"]     # Ignorar elementos con style="display:none"
# }

# # Generar la estructura optimizada
# esquema = generar_esquema_jerarquico(elemento_base, excluir_tags)

# # Mostrar el esquema limpio en formato legible
# print(esquema)
# mostrar_esquema(esquema)
