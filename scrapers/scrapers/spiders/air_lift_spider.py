import requests
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor

class AirLiftSpider(CrawlSpider):
    
    name = 'airlift'
    
    start_urls ={
        'https://www.airliftexpress.com/',
    }
    
    rules = (
        Rule(LinkExtractor(restrict_css='a.pcm-link'), callback='parse_product', follow=False),
    )
    
    custom_request_headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0',
        'Accept': 'application/json, text/plain, */*',
        'access-key': 'f0f0682a-20db-4c63-aa12-d9214a0c5203'
    }
    
    def parse_product(self, response):
        page = 1
        product_category = response.url.split('/')[-1]
        
        try:
            product_response = self.get_products_from_page(product_category, page)
        except:
            return
        
        for product in product_response.json():
            yield product
            
        while len(product_response.json()) != 0:
            page += 1
            product_response = self.get_products_from_page(product_category, page)
            for product in product_response.json():
                yield product
        
    def get_products_from_page(self, product_category, page):
        products_url = f'https://storeapi.airliftgrocer.com/v2/products?categorySlug={product_category}&per_page=25&page={page}'
        product_response = requests.request(method="GET", url=products_url, headers=self.custom_request_headers)
        return product_response
