
from urllib import parse
from urllib import robotparser
from urllib.request import Request
from urllib.request import urlopen

#
# clase Download: utilizada para la descarga de páginas de interés
# 
#  La creación de la instancia inicial permite especificar la dirección base del site (donde ubicar robots.txt y
#  contra la que se aplicará cualquier control de throttling), y el Agente a especificar durante el acceso al site.
#
#  método __init__(): Constructor de la clase, y solo mantiene registro de los valores iniciales de los atributos
#  método get()     : recibe el URL de la página que será objeto de descarga, y ejecuta los siguientes pasos
#                  a. Inicializa el Header para el Request Inicial al Servidor, especificando el Agente indicado
#                  b. Toma el archivo robots.txt del site y lo parsea para propósitos de validación
#                  c. Se ensambla REquest inicial al site, especificando en el header el Agente indicado
#                  d. Se valida en el archivo robots.txt si existe alguna restricción para el Agente sobre la URL de interes
#                  e. Descarga de la página en caso afirmativo
#                  F. RETORNO código html de la página.
#

class Download:

    def __init__(self, url_base, user_agent='wswp' ):
	     self.user_agent = user_agent         # Denominación especificada para creación del Agente para Scraping
		 self.url_base = url_base             # URLbase del Site anfitrión
         self.url = ""                        # URL objeto de la descarga
		 
    def get(self, url):
        print('Downloading:', url)
        headers = {'User-agent': self.user_agent}	 # Preparación del Header a ser incluido en el Request de Inicio
		                                             # que incluye el Registro del Agente a utilizar durante la operación
													 
		# En vista de lo pequeño de este tipo de archivos, tiene sentido complicar la tarea manteniendo 
		# una copia local durante el acceso, así que se accesa cada vez que desea navegarse por alguna página del site
		
	    rp = robotparser.RobotFileParser()           # Inicializa objeto para parsing de robots.txt 
        rp.set_url(parse.urljoin(self.url_base, 'robots.txt'))  # establece la ruta de acceso al archivo usando URL Base
        rp.read()                                    # Lectura del archivo
		
		self.url = url                         # Se almacena en la instancia del objeto, el site que será descargado
		
        r = Request(url, headers=headers)      # Ensambla Request inicial, utilizando el header que indica el Agente
 
        if rp.can_fetch(self.user_agent, url): # Validación sobre robots.txt de restricciones del Agente sobre el URL
            html = urlopen(r).read()           # Descarga de la página indicada en la URL
		else:
			print('Conetnido bloqueado por robots.txt:', url)
		  
        return html                            # Retorno de la página en caso de no existir restricciones de acceso