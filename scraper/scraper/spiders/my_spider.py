import scrapy
import json
import time

class MySpider(scrapy.Spider):
    name = 'my_spider'
    # start_urls = ['https://example.com/api/data.json']  # Replace with your target URL
    start_urls = ['https://www.sreality.cz/api/en/v2/estates?category_main_cb=1&category_type_cb=1&locality_region_id=10&per_page=2&tms='
                  +str(int(time.time() * 1000))]

    def parse(self, response):
        # Check if the response is JSON (adjust content type as needed)
        # if 'application/json' in response.headers.get('Content-Type').decode('utf-8'):
            data = json.loads(response.text)

            # Process the JSON data (example: print first item)
            estates = data["_embedded"]["estates"]
            for estate in estates:
                self.log(f'First item: {estate["name"]}')

        # else:
        #     self.log('Response is not JSON.')
        #     self.log(response.text) 
            

