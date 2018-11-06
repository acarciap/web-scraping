import urllib
from urllib.request import urlopen # urllib2
from urllib.parse import urlparse 
import datetime
import time

#
# clase Throttle: utilizada para controlar los tiempos de espera indicados por las políticas sugeridas 
#                 por el propietario del site, en el archivo robots.txt.
# 
#  La creación de la instancia inicial permite especificar el valor del parámetro de espera para el site,
#  que será utilizado el control de throttling, aplicable directamente sobre la url_base, indpendientemente de 
#  la url que se desea accesar.
#
#  método __init__(): Constructor de la clase, y solo mantiene registro de los valores iniciales de los atributos
#  método wait()    : No recibe parámetros, y sólo determina la diferencia en segundos de la hora actual, versus el
#                     registro del último acceso. En caso de no superar el tiempo de espera, duerme el hilo de
#                     de ejecución por la difrencia (espera), para finalmente proseguir con la ejecucíón (almacenando 
#                     lo que será el próximo valor del último acceso -- hora actual)
#         
#                     Debe ser invocado antes de la descarga (Download) de cualquier página ...
#
class Throttle:
    def __init__(self, delay):
        self.delay = delay       # Valor de Espera especificado para control de accesos
		self.tiempo = None       # Registro del instante del último acceso
	   
    def wait(self):
	    #
        # Si se ha especificado un tiempo de espera y se dispone ya de un priemr acceso, 
		# se procede a la validación de control de throttling
		#
        if self.delay > 0 and self.tiempo is not None:  
		    #
		    # el waiting time se obtiene al restar al tiemo de espera  
			# el tiempo transcurrida desde el último acceso (i.e., la diferencia entre 
			# la hora actual y el último acceso registrado) 
			#
			# El resultado (de ser positivo) es el número de segundos a retener el proceso
			#
            receso=self.delay-(datetime.datetime.now()-self.tiempo ).seconds
            if receso > 0:
                time.sleep(receso) 
		#
		# Registro del último acceso
		#
        self.tiempo = datetime.datetime.now()