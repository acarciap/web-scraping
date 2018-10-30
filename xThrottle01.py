import urllib
from urllib.request import urlopen # urllib2
from urllib.parse import urlparse # urllib2
import datetime
import time

class Throttle:
    def __init__(self, delay):
        self.delay = delay
		self.tiempo = None
	   
    def wait(self):
        		
        if self.delay > 0 and self.tiempo is not None:
            receso=self.delay-(datetime.datetime.now()-self.tiempo ).seconds
            if receso > 0:
                time.sleep(receso) 
        self.tiempo = datetime.datetime.now()