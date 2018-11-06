
#
# Objeto PIB
#
# Accesa y parsea la página 'https://datosmacro.expansion.com/pib', con la finalidad de determinar
# la URL de la página en la que se encuentra la información de crecimiento económico para cada país,
# con la finalidad de extraer la información publicada para el año especificado por el usuario,
# siempre en el rango comprendido entre 1990 y 2018.
#
# Forma de Uso
# Al crear la instancia, se especifica la URL base del site (sobre el que se controlará la restricción
# de acceso en relación al throttling), y opcionalmente el tiempo de espera indicado en los términos
# especificados por el propietario del site, sobre el archivo robots.txt (por defecto toma 10 segundos).
#
# Una vez disponible la instancia, se invoca el método getPIB() con el año y la URL de interés. Al
# finalizar el procesamiento el método retorna una estructura de tipo DataFrame con las columnas siguientes:
#
#     anio        Año para el que se requiere la información
#     pais        Denominiación del país al que corresponde el registro
#     pib         Valor reportado para el Producto Interno Bruto Pais
#     var_pib     Variación del PIB país con respecto al año previo
#     pib pc      Valor calculado del PIB per cápita para el año reportado
#     var_pib pc  Variación porcentual del PIB er cápita con respecto al año previo
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
# Ubicado el listado de paises reportados en la página, se itera sobre cada uno extrayéndo la URL hacia la  
# página auxiliar que despliega la información general y per cápita del país. 
#
# Se descarga esta segunda página adheriendose a las indicaciones descritas en el archico robots.txt, y se
# extrae de la misma la información requerida para el año de la búsqueda.
#
# Los datos así obtenidos, son sistemáticamente depurados y dispuestos en listas, que finalmente serán utilizadas 
# para confeccionar las columnas de la estructura dataframe de retorno.
#
from urllib.parse import urljoin 

from bs4 import BeautifulSoup
import pandas as pd

#from DownLoad import Download
#from Throttle import Throttle

class PIB:
# 'https://datosmacro.expansion.com/pib'

    def __init__(self, url_base, delay = 10):	    
        self.url_base = url_base 
        self.delay = delay

    def getPIB(self, year, xURL ):		
	    year_min = 1990
		year_max = 2018
	    #
	    # Declaración de nuestro agente de acceso ...
	    agente = 'MyAgent'
	    #
		# Inicialización de los objetos necesarios para el control de throttling y descarga
        throttle = Throttle(self.delay)
        xhtml = Download(self.url_base, user_agent=agente)
		#
		# Inicialización de las listas que contendrán cada columna a retornar		
		col01 = []
		col02 = []
		col03 = []
		col04 = []
		col05 = []
		col06 = []
		#
		# Verificación del rango de fechas a la que se da soporte  con el algoritmo ...		
		if year > year_max:
		   print('Se excede el rango máximo de búsqueda... operación suspendida ...')
		   return
		   
		if year < year_min:
		   print('Parámetro de búsqueda muy bajo... operación suspendida ...')
		   return
		#
		# Ubica la tabulación de paises para el año de interés, mediante navegación de los
		# enlaces que organizan la exposición de la información en la página.
		#
		# Sucesivamente se extraen las páginas correspondiente años previos, hasta llegar
		# al año objeto de la búsqueda.
		#				
		anioIni = 9999
		
		auxURL = xURL
		
        while year < anioIni :                          # Mientras no se ubique el año se navega por las paginas del site
		    throttle.wait( )		                    #    Verificación de tiempo de espera versus última descarga registrada
            html = xhtml.get(auxURL)                    #    Descarga de la página de interés
		
            soup = BeautifulSoup(html, 'lxml')          #    Parseo del html correspondiente para verificación de año

            txtanio = soup.find(class_="tablefooter")   #    Ubicación de la clase que incluye link al año previo

            txtanioIni = txtanio.span.a.text            #    Extracción del año previo a partir del link navegación
            anioIni = int(txtanioIni[-4:])+1            

            auxURL = txtanio.span.a['href']             #    Ref para la extracción de la página del año previo, en caso
			auxURL = parse.urljoin(xURL, auxURL)        #    de no haber ubicado ya el año de interes, y construcción de URL absoluta

		#
		# Ubicada la página correspondiente al año, se ubica la tabla que organiza los links
        # hacia cada pais, en los que se expone de forma individual la información de interés
        tb = soup.table.tbody
		#
		# se prepara un segundo objeto de descarga, para obtener la página individual de cada pais
        yhtml = Download(self.url_base, user_agent=agente)
	
	    #
		# para cada registro listado en la página principal(correspondiente a cada pais) reportado
		# se extrae el link de la pagina que desgloza su información individual, para luego
		# descargar esta sgunda página y extraer la información requerida.
		#
        for e in tb.find_all('a'):                    # Para todos los paises listados en la pagina principal
            pais   = e.text.split()[0]                #     Obtener denominación del pais correspondinete a la entrada actual
	        url_pais = e.get('href')                  #     Obtener la URL a la página auxiliar que despliega inf. del pais 
			
            url_pais = parse.urljoin(xURL, url_pais)  #     Construir URL abosoluta correspondiente
			
		    throttle.wait()		                      #     Verificación de tiempo de espera versus la descarga previa
            html_pais = yhtml.get( url_pais )         #     Descarga de la página correspondiente al país en turno

	        soup_pais = BeautifulSoup(html_pais, 'lxml')  # Parseo del html correspondiente al URL del país
	        #
			# Inspección de las entradas correspndientes a la clase table-responsive presentes en la página auxiliar.
			# Pueden haber varias de ellas, pero solo importan dos: Deben obviarse todas las presenten información
			# específica del trimestre, en beneficio de las que especifican información para todo el año.
			#
	        tb2 = soup_pais.find_all(class_="table-responsive")
			
	        data = []   # <- almacena los valores extraidos para el país, y por cada nuevo pais que se inspecciona, 
			            #    se reinicializa a vacio, facilitando el control y manejo de los datos extraidos
	
	        for eg in tb2:                        # Para cada tabla presente en la página auxiliar debe verficarse
	            tb2_dg = eg.tbody                 # obtener contenido de la tabla
									
                for eg_dg in tb2_dg.children:	              # Para cada entrada del contenido recién obtenido		
		            anio_dg = eg_dg.find(class_="fecha").text #    Tomar texto indicativo del período al que corresponde 
			                                                  #    la información
			        try:
					    #
					    # Si la tabla corresponde a datos trimestrales, la conversion falla, y pasa se pasa a la siguiente.
						# Si la conversion es exitosa, la tabla contiene datos anuales de interés, y se procesa su contenido.
						#
                        if int(anio_dg) == year:   # En el contexto de tablas con información anual, se itera
                            					   # sobre las entradas que van siendo extraidas, hasta ubicar
				            pib = ""               # la que corresponde con el año de interés especificado por
					        var_pib = ""           # el usuario.
					
					        # Extracción de los campos de interés ...
                            #							
					        # Interpretación de las clases de las tablas con información anual, para
							# determinar los campos a los que corresponde asignar el valor extraido.
							#
							# De las dos tablas que interesan, la primera expone información degenral del pais;
							# mientras que la segunda, presenta expone la información per cápita requerida
							#
							# En cualquier caso, existe un conflicto de nombres en la denominación de los campos
							# del que hay que cuidar durante el parseo...
							#
				            for etr in eg_dg.children:					    
						        if etr['class'] == ['fecha'] or etr['class'] == ['numero','dol']:
						           pass
						        elif etr['class'] == ['numero']:						
						           var_pib = etr.text
						        elif etr['class'] == ['numero','eur'] and len(pib)==0:
						           pib = etr.text					    
						        else:
						           var_pib = etr.text
 			                #
			                # Ajustes de Formato ...
			                if pib == None or len(pib) == 0:
	                            pib = '0'
	                        else:
	                            pib = pib.replace("€","")
                                pib = pib.replace("M","")						
	                            pib = pib.replace(".", "")
	                            pib = pib.replace(",", ".")

			                if var_pib == None or len(var_pib) == 0:
	                            var_pib = '0'
	                        else:
	                            var_pib = var_pib.replace("%","")	   
	                            var_pib = var_pib.replace(".", "")
	                            var_pib = var_pib.replace(",", ".")
														
			                if data:	
							    # Si se presenta con algun contenido la lista data, implica que la 
								# 1ra tabal con inforamción general del país ya fue procesada.
								#
								# en consecuencia, estamos en presencia de los datos correspondientes
								# a la segunda tabla del pais con información per cápita.
								#
                                col05.append(float(pib))
								col06.append(float(var_pib))								
							else: 
							    #
								# Captura de datos generales al pais (1ra Tabla de interés)
								# se inicializa la lista de acopio data con el valor de las 
								# primeras columnas para el país en curso ...
								
                                data = [ int(anio_dg), pais, float(pib), float(var_pib) ]
								
								col01.append(int(anio_dg))
								col02.append(pais)
								col03.append(float(pib))
								col04.append(float(var_pib))															
	                except:
					    # Este es el caso necesario para omitir el procesamiento de las tablas secundarias
						# con los resumenes trimestrales por pais, que no resultan de interés para la extracción.
						#
			            pass
		#
        # Finalizado el barrido de links enumerados en la la ágian principal, las listas col0<i>, mantienen todas
        # la información necesaria para la construcción del dataframe de salida, cuya confección sigue a continuación
        #		
	    datos = {'anio': col01, 'pais': col02, 'pib': col03, 'var_pib': col04, 'pib pc': col05, 'var_pib pc': col06}
		dfData = pd.DataFrame( datos )
			
		return dfData