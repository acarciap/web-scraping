
from bs4 import BeautifulSoup
import pandas as pd

#from DownLoad import Download
#from Throttle import Throttle

class SalarioMinimo:

    def __init__(self, url_base, delay = 10):
	    
        self.url_base = url_base # 'https://datosmacro.expansion.com/smi'
        self.delay = delay

    def getSMI(self, year, xURL ):
        throttle = Throttle(self.delay)
        xhtml = Download(self.url_base, user_agent='MyAgent')
		
		col01 = []
		col02 = []
		col03 = []
		col04 = []
		col05 = []
		
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
            pais    = e.a.text.split()[0]
	        anio    = e.find(class_="fecha").text
	        smi_lo  = e.find(class_="numero").text
	        smi_eu  = e.find(class_="numero eur").text
	        var_smi = e.find(class_="numero text-pos")

	        smi_lo = smi_lo.replace(".", "")
	        smi_lo = smi_lo.replace(",", ".")
	
	        if smi_eu == None or len(smi_eu) == 0:
	            smi_eu = 0
	        else:
	            smi_eu = smi_eu.split()[0] 
		        smi_eu = smi_eu.replace(".", "")
		        smi_eu = smi_eu.replace(",", ".")

	        if var_smi == None or len(var_smi) == 0:
	           var_smi = 0
	        else:
	           var_smi = var_smi.text.replace("%","")	   
	           var_smi = var_smi.replace(".", "")
	           var_smi = var_smi.replace(",", ".")		
		
		    col01.append(int(anioIni))
			col02.append(pais)
			col03.append(float(smi_lo))
			col04.append(float(smi_eu))
			col05.append(float(var_smi))
			
        data = {'anio': col01, 'pais': col02, 'smi': col03, 'smi_eu': col04,'var_smi': col05}
		df = pd.DataFrame( data )
		
		return df
	
	    
	
