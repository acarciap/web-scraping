#import urllib
#from urllib.request import urlopen # urllib2

from bs4 import BeautifulSoup
import pandas as pd

#from DownLoad import Download
#from Throttle import Throttle

class SalarioMedio:

    def __init__(self, url_base, delay = 10):
	    
        self.url_base = url_base # 'https://datosmacro.expansion.com/mercado-laboral/salario-medio'
        self.delay = delay

    def getSM(self, year, xURL ):
        throttle = Throttle(self.delay)
        xhtml = Download(self.url_base, user_agent='MyAgent')
		
		col01 = []
		col02 = []
		col03 = []
		col04 = []
		
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

            txtanio = soup.find(class_="tabletit")

            txtanioIni = txtanio.span.a.text
            anioIni = int(txtanioIni[-4:])+1	
			
            auxURL = txtanio.span.a['href']
			auxURL = parse.urljoin(xURL, auxURL)

        tb = soup.table.tbody

        for e in tb.children:
            pais   = e.a.text.split()[0]
        	sm_eu  = e.find(class_="numero eur").text
        	var_sm = e.find(class_="numero text-pos")
		
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
		
		    col01.append(int(anioIni))
			col02.append(pais)
			col03.append(float(sm_eu))
			col04.append(float(var_sm))
			
        data = {'anio': col01, 'pais': col02, 'sm': col03, 'sm_eu': col04}
		df = pd.DataFrame( data )
		
		return df
