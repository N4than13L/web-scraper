import csv 
import requests
from bs4 import BeautifulSoup
from fpdf import FPDF
import pdfkit
import os 

def obtener_html(url):
    """ 
    Obtiene el HTML de una página web (HTML)
    ARGs: Url fr la pagina a obtener el HTML
    returns str del copntenido html de la pagina none o si hay un error 
    """

    try:
        # configurar el user-agent para evitar bloqueos por parte del servidor
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        # realizar petición GET a la URL con un timeout de 10 segundos
        respuesta = requests.get(url, headers=headers, timeout=10)

        # verificar que la respuesta fue exitosa (código 200)
        if respuesta.status_code == 200:
            return respuesta.text
        else:
            print(f"Error al obtener el HTML: Código de estado {respuesta.status_code}")
            return None
        

    except Exception as e:
        print(f"Error al obtener la pagina: {e}")
        return None

def extraer_titulos_web(html):
    """
    Extrae los títulos de una página web (list)
    ARGs: html str del contenido html de la pagina
    
    returns list de titulos encontrados en la pagina
    """

    #crear un objeto BeautifulSoup para analizar el HTML
    soup = BeautifulSoup(html, 'html.parser')

    # encontrar todos los elementos de título de la web 
    #Nota: Estos selectores son genericos y pueden necesitar ajustes según la estructura de la página web específica
    titulos = []

    # buscar títulos en etiquetas h1, h2 y h3 que podrian contener titulos 
    for heading in soup.find_all(['h1', 'h2', 'h3']):
        # filtrar solo los elemtnos que contienen contenido relevante con cierta longitud 
        if heading.text.strip() and len(heading.text.strip()) > 10:
            titulos.append(heading.text.strip())


# buscar tambien en elementos con clases comunes para titulos de noticias o articulos
    for elemento in soup.select('.title, .headline, .article-title, .news-title'):
        if elemento.text.strip() and elemento.text.strip() not in titulos:
            titulos.append(elemento.text.strip())
    return titulos


def extraer_articulos(html):
    """
    Extrae los artículos de una página web (list)
    ARGs: html str del contenido html de la pagina
    
    returns list de articulos encontrados en la pagina
    """

    #crear un objeto BeautifulSoup para analizar el HTML
    soup = BeautifulSoup(html, 'html.parser')

    # encontrar todos los elementos de artículo de la web 
    #Nota: Estos selectores son genericos y pueden necesitar ajustes según la estructura de la página web específica
    articulos = []

    # buscar artículos en etiquetas p que podrian contener contenido relevante 
    for articulo_elem in soup.select('article, .article, .post, .news-item, .newpage p, .article-content div'):
        articulo = {}

        # extraer el título del artículo si está disponible
        titulo_elem = articulo_elem.find(['h1', 'h2', 'h3',]) or articulo_elem.select_one('.title, .headline')

        if titulo_elem:
            articulo['titulo'] = titulo_elem.text.strip()
        else:
            continue  # Si no hay título, saltar este artículo

        # extraer la fecha del artículo
        fecha_elem = articulo_elem.select_one('.date, .published-date, .post-date, .news-date, .timestamp')
        articulo['fecha'] = fecha_elem.text.strip() if fecha_elem else ""

        # extraer resumen del contenido del artículo
        resumen_elem = articulo_elem.select_one('.summary, .excerpt, .description, .snippet, p')  # Tomar el primer párrafo como resumen
        articulo['resumen'] = resumen_elem.text.strip() if resumen_elem else ""

    # extraer contenido del contenido del artículo
        contenido = articulo_elem.select_one('div .article-content, .outer_page_container, .newpage, span .a-price-whole')  # Tomar el primer párrafo como resumen
        articulo['contenido'] = contenido.text.strip() if contenido else ""
        if contenido:
            articulo['contenido'] = contenido.text.strip()
        else:
            continue  # Si no hay título, saltar este artículo

        articulos.append(articulo)
        # articulos.append(contenido)

        # agregar el artículo a la lista si tiene título y resumen
    return articulos
    
html = obtener_html("https://www.amazon.com/s?k=ryzen+7+9800x%2B3d&crid=31FZTVY8HKFJJ&sprefix=ryzen+%2Caps%2C174&ref=nb_sb_ss_p13n-expert-pd-ops-ranker_1_6")

print(extraer_titulos_web(html))

