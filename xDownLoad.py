
from urllib import parse
from urllib import robotparser
from urllib.request import Request
from urllib.request import urlopen

class Download:

    def __init__( self, url_base, user_agent='wswp', num_retries=2 ):
	     self.user_agent = user_agent
		 self.num_retries = num_retries
		 self.url_base = url_base
         self.url = ""
		 self.url_crawl = ""
		 
    def get(self, url):
        print('Downloading:', url)
        headers = {'User-agent': self.user_agent}	
		
	    rp = robotparser.RobotFileParser()
        rp.set_url(parse.urljoin(self.url_base, 'robots.txt'))
        rp.read()
		
		self.url = url
		
        r = Request(url, headers=headers)             
 
        if rp.can_fetch(self.user_agent, url):
            html = urlopen(r).read()            			   
		else:
			print('Conetnido bloqueado por robots.txt:', url)
		  
        return html