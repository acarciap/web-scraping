import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
#from PyQt5.QtWebEngineWidgets import QWebEnginePage

from PyQt5.QtCore import QEventLoop

class Render(QWebEngineView):
#class Render(QWebEnginePage):
    def __init__(self, url):
        self.html = None
        self.app = QApplication(sys.argv)
		
        QWebEngineView.__init__(self)
        #QWebEnginePage.__init__(self)
		
		loop = QEventLoop()
		
        self.loadFinished.connect(self._loadFinished)
				
        self.load(QUrl(url))
		loop.exec_()
		
		self.show()		
		
        self.app.exec_()
 

    def _loadFinished(self, result):
        # This is an async call, you need to wait for this
        # to be called before closing the app
        self.page().toHtml(self._callable)
		#self.toHtml(self._callable)
		self.app.quit()


    def _callable(self, data):
        self.html = data
		filename = ".\\dm\\etc\\Qt - ensayo\\html\\x.html"
		with open(filename, 'a+') as f:
		    f.write(data)
		
		
xURL = 'http://appsso.eurostat.ec.europa.eu/nui/show.do?dataset=nama_10_gdp&lang=en'
t = Render(xURL)