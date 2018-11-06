
#
# Objeto SalarioMedio
#
# Accesa y parsea la página 'https://datosmacro.expansion.com/mercado-laboral/salario-medio'
# con la finalidad de extraer información publicada para el año especificado por el usuario,
# en el rango comprendido entre 1990 y 2018.
#
# Forma de Uso
# Al crear la instancia, se especifica la URL base del site (sobre el que se controlará la restricción
# de acceso en relación al throttling), y opcionalmente el tiempo de espera indicado en los términos
# especificados por el propietario del site, sobre el archivo robots.txt (por defecto toma 10 segundos).
#
# Una vez disponible la instancia, se invoca el método getSM() con el año y la URL de interés. Al
# finalizar el procesamiento el método retorna una estructura de tipo DataFrame con las columnas siguientes:
#
#     anio     Año para el que se requiere la información
#     pais     Denominiación del país al que corresponde el registro
#     sm_eu    Importe del Salario Medio en euros
#     var_sm   Variación porcentual del Salario Medio con respecto al año previo
#     
# Dependencias
# módulo Throttle: provisto con la implementación actual, soporta las políticas de control de throttling
# módulo Download: provistos con la implementación actual, ejecuta las descarga verificando Agente vs robots.txt
#
# Funcionalidad
# La creación de la instancia inicializa las variables básicas para la adherencia a las políticas de acceso
# indicadas por el propietario del site, a través de la configuración del archivo robots.txt. 
#
# Tales variables se limitan a: Especificación del URL base (url de inicio del site)
#                               Tiempo de Espera para control de throttling
#
# La invocación del método get de la instancia, crea a su vez las instancias que se requieren de los objetos
# Throttle y Download, que garantizan la adherencia a las políticas de acceso al site.
#
# El procesamiento se inicia validando el año requerido en la página inicial descargada, y en caso de que la
# información no se corresponda con la del año de interés, se descarga la página correspondiente al año previo.
# Se itera sucesivamente de esta forma, hasta lograr el contenido del año especificado por el usuario.
#
# Se extrae la tabla que organiza la información, y para cada entrada se extraen los datos objeto de la descarga.
# éstos son depurados y dispuestos en listas, que finalmente serán utilizadas para confeccionar las columnas de
# la estructura dataframe de retorno.
#
from bs4 import BeautifulSoup
import pandas as pd

#from DownLoad import Download
#from Throttle import Throttle

class SalarioMedio:
# 'https://datosmacro.expansion.com/mercado-laboral/salario-medio'

    def __init__(self, url_base, delay = 10):	    
        self.url_base = url_base 
        self.delay = delay

    def getSM(self, year, xURL ):
	    year_min = 1990
		year_max = 2018
	    #
		# Inicialización de los objetos necesarios para el control de throttling y descarga
        throttle = Throttle(self.delay)
        xhtml = Download(self.url_base, user_agent='MyAgent')		
		#
		# Inicialización de las listas que contendrán cada columna a retornar
		col01 = []
		col02 = []
		col03 = []
		col04 = []
		#
		# Verificación del rango de fechas a la que se da soporte  con el algoritmo ...		
		if year > year_max:
		   print('Se excede el rango máximo de búsqueda... operación suspendida ...')
		   return
		   
		if year < year_min:
		   print('Parámetro de búsqueda muy bajo... operación suspendida ...')
		   return
		#
		# Ubicación de los datos correspondientes al año de interés, mediante navegación de los
		# enlaces que organizan la exposición de la información en la página.
		#
		# Sucesivamente se extraen las páginas correspondiente años previos, hasta llegar
		# al año objeto de la búsqueda.
		#		
		anioIni = 9999
		
		auxURL = xURL
		
        while year < anioIni :                     # Mientras no se ubique el año se navega por las paginas del site
		    throttle.wait( )		               #    Verificación de tiempo de espera versus última descarga registrada
            html = xhtml.get(auxURL)               #    Descarga de la página de interés
		
            soup = BeautifulSoup(html, 'lxml')     #    Parseo del html correspondiente para verificación de año

            txtanio = soup.find(class_="tabletit") #    Ubicación de la clase que incluye link al año previo

            txtanioIni = txtanio.span.a.text       #    Extracción del año previo a partir del link navegación
            anioIni = int(txtanioIni[-4:])+1	
			
            auxURL = txtanio.span.a['href']        #    Ref para la extracción de la página del año previo, en caso
			auxURL = parse.urljoin(xURL, auxURL)   #    de no haber ubicado ya el año de interes, y construcción de URL absoluta
		#
		# Ubicada la página correspondiente al año, se ubica la tabla que organiza los datos de interés
        tb = soup.table.tbody
		
		#
		# Para cada entrada de la tabla: extraer los datos de interes, depurarlos, e incorporarlosa las listas de salida 
        for e in tb.children:
		    #
			# Extracción de los campos de interés ...
            pais   = e.a.text.split()[0]
        	sm_eu  = e.find(class_="numero eur").text
        	var_sm = e.find(class_="numero text-pos")
		
 			#
			# Ajustes de Formato ...
         	if sm_eu == None or len(sm_eu) == 0:
        	    sm_eu = 0
        	else:
                sm_eu = sm_eu.replace("€","")		
        		sm_eu = sm_eu.replace(".", "")
        		sm_eu = sm_eu.replace(",", ".")

        	if var_sm == None or len(var_sm) == 0:
        	   var_sm = 0
        	else:
        	   var_sm = var_sm.text.replace("%","")	   
        	   var_sm = var_sm.replace(".", "")
        	   var_sm = var_sm.replace(",", ".")
			   
		    #
			# Incorporación de valores obtenidos a las listas de salida ...
		    col01.append(int(anioIni))
			col02.append(pais)
			col03.append(float(sm_eu))
			col04.append(float(var_sm))
        #
        # Al concluir el ciclo de extracción (agotadas todas las entradas de la tabla), utilizando las listas de 
		# valores obtenidos como columnas, se confecciona la estructura de tipo diccinario para construir el dataframe
		# de salida.
		
        data = {'anio': col01, 'pais': col02, 'sm_eu': col03, 'var_sm': col04}
		df = pd.DataFrame( data )
		
		return df
