import requests
from bs4 import BeautifulSoup
import re
from io import BytesIO
from PIL import Image
import time

URL_DESCARGA = "https://www.flipsnack.com/utahstate/gu-a-para-estudiantes-y-padres-de-familia.html"
RUTA_PDF = "drive/MyDrive/flipsnack/folleto_utah.pdf"
TIEMPO_ESPERA = 3

def flipsnack_pdf():
  with requests.Session() as cliente:
    cliente.headers = {
      'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
      'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
      'Connection': 'keep-alive',
      'Upgrade-Insecure-Requests': '1',
      'Sec-Fetch-Dest': 'document',
      'Sec-Fetch-Mode': 'navigate',
      'Sec-Fetch-Site': 'none',
      'Sec-Fetch-User': '?1',
      'Pragma': 'no-cache',
      'Cache-Control': 'no-cache'
    }

    peticion = cliente.get(URL_DESCARGA, timeout=7)
    if peticion.status_code != 200:
      print(f"ERROR: status code incorrecto {peticion.status_code} al comprobar {URL_DESCARGA}")
      return
    soup = BeautifulSoup(peticion.text, "html.parser")
    meta_info = soup.select_one("meta[name='image']")
    if meta_info == None:
      print("ERROR: no se ha encontrado la etiqueta meta necesaria para obtener el identificador de la publicación")
      return
    meta_url = meta_info.attrs["content"]
    identificador = re.sub(r"https.*?items/(.*?)/cover.*", r"\1", meta_url)
    
    paginas_publicacion = []
    contador = 1
    while True:
      url = f"https://cdn.flipsnack.com/collections/items/{identificador}/covers/page_{contador}/original"
      peticion = cliente.get(url, timeout=7)
      if peticion.status_code != 200:
        break
      print(f"Página {contador} descargada...")
      pagina = Image.open(BytesIO(peticion.content))
      paginas_publicacion.append(pagina)
      contador += 1
      time.sleep(TIEMPO_ESPERA)

    paginas_publicacion[0].save(RUTA_PDF, "PDF" ,resolution=100.0, save_all=True, append_images=paginas_publicacion[1:])

  print("FIN")
      
flipsnack_pdf()