#import urllib
#from urllib.request import urlopen # urllib2
from urllib.parse import urljoin # urllib2

from bs4 import BeautifulSoup
import pandas as pd

#from DownLoad import Download
#from Throttle import Throttle


class PIB:

    def __init__(self, url_base, delay = 10):
	    
        self.url_base = url_base # 'https://datosmacro.expansion.com/pib
        self.delay = delay

    def getPIB(self, year, xURL ):
	    agente = 'MyAgent'

        throttle = Throttle(self.delay)
        xhtml = Download(self.url_base, user_agent=agente)
		
		col01 = []
		col02 = []
		col03 = []
		col04 = []
		col05 = []
		col06 = []
		
		if year > 2018:
		   print('Se excede el rango máximo de búsqueda... operación suspendida ...')
		   return
		   
		if year < 1990:
		   print('Parámetro de búsqueda muy bajo... operación suspendida ...')
		   return
		
		anioIni = 9999
		
		auxURL = xURL
		
        while year < anioIni :
		    throttle.wait( )		
            html = xhtml.get(auxURL)
		
            soup = BeautifulSoup(html, 'lxml')

            txtanio = soup.find(class_="tablefooter")

            txtanioIni = txtanio.span.a.text
            anioIni = int(txtanioIni[-4:])+1

            auxURL = txtanio.span.a['href']
			auxURL = parse.urljoin(xURL, auxURL)

        tb = soup.table.tbody
        yhtml = Download(self.url_base, user_agent=agente)
	
        for e in tb.find_all('a'):                 # Para todos los paises
            pais   = e.text.split()[0]
	        url_pais = e.get('href')
			
            url_pais = parse.urljoin(xURL, url_pais)
			
		    throttle.wait( )		
            html_pais = yhtml.get( url_pais )

	        soup_pais = BeautifulSoup(html_pais, 'lxml')
	
	        tb2 = soup_pais.find_all(class_="table-responsive")
	        data = []
	
	        for eg in tb2:                        # Para todas las Tablas
	            tb2_dg = eg.tbody
									
                for eg_dg in tb2_dg.children:			
		            anio_dg = eg_dg.find(class_="fecha").text
			
			        try:
                        if int(anio_dg) == year:
                            						
				            pib = ""
					        var_pib = ""
					
				            for etr in eg_dg.children:					    
						        if etr['class'] == ['fecha'] or etr['class'] == ['numero','dol']:
						           pass
						        elif etr['class'] == ['numero']:						
						           var_pib = etr.text
						        elif etr['class'] == ['numero','eur'] and len(pib)==0:
						           pib = etr.text					    
						        else:
						           var_pib = etr.text
							
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
                                col05.append(float(pib))
								col06.append(float(var_pib))								
							else: 
                                data = [ int(anio_dg), pais, float(pib), float(var_pib) ]
								
								col01.append(int(anio_dg))
								col02.append(pais)
								col03.append(float(pib))
								col04.append(float(var_pib))															
	                except:
			            pass
				
	    datos = {'anio': col01, 'pais': col02, 'pib': col03, 'var_pib': col04, 'pib pc': col05, 'var_pib pc': col06}
		dfData = pd.DataFrame( datos )
			
		return dfData