
import scrapy

from selenium import webdriver

class bEconSpider(scrapy.Spider):
    name = 'eu_bEconSpider'
    start_urls = ["http://appsso.eurostat.ec.europa.eu/nui/show.do?dataset=nama_10_gdp&lang=en"]   

    # Initalize the webdriver    
    def __init__(self):
        self.driver = webdriver.Firefox()
		
    # Parse through each Start URLs
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)    
    

   # Parse function: Scrape the webpage and store it
   
    def parse(self, response):
        self.driver.get(response.url)
        filename =".\\dm\\etc\\Qt - ensayo\\html\\becon_data.html"
        with open(filename, 'w') as f:
            f.write(response.body)
			
