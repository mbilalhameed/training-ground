import re
from scrapy.http import request
from scrapy.spiders import Rule, CrawlSpider, Request
from scrapy.linkextractors import LinkExtractor

class SehgalMotorSpider(CrawlSpider):
    
    name = 'sapphire'
    start_urls = ['https://pk.sapphireonline.pk/', ]
    allowed_domain = 'sapphireonline.pk'
    
    rules = (
        Rule(LinkExtractor(allow = 'collections/' ,restrict_css="ul#nt_menu_id"), callback="parse_collections" , follow=True),
    )
    
    regex = re.compile(r'[\n\r\t ]+')
        
    def parse_collections(self, response):
        next_page_url = self.get_next_page_url(response)
        if next_page_url:
            yield Request(url=next_page_url, callback=self.parse_collections)
        products_links = response.css("div.product-inner div.product-image::attr(data-include)").getall()
        for product_link in products_links:
            product_request_link = self.start_urls[0] + product_link.split('?')[0]
            yield Request(url=product_request_link, callback=self.parse_product)
    
    def parse_product(self, response):
        yield self.scrap_products_info(response)
    
    def scrap_products_info(self, response):
        product_link = response.url
        product_name = self.get_product_name(response)
        product_category = self.get_product_category(response)
        product_sku = self.get_product_sku(response)
        product_price = self.get_product_price(response)
        product_availability = self.get_product_availability(response)
        product_available_sizes = self.get_product_available_sizes(response)
        product_details = self.get_product_details(response)
        product_size_chart = self.get_product_size_chart(response)
        product_shipping_return_policy = self.get_shipping_return_policy(response)
        
        return {
            'product_link': product_link,
            'product_name': product_name,
            'product_category': product_category,
            'product_sku': product_sku,
            'product_price': product_price,
            'product_availability': product_availability,
            'product_available_sizes': product_available_sizes,
            'product_details': product_details,
            'product_size_chart': product_size_chart,
            'product_shipping_return_policy': product_shipping_return_policy
        }
    
    def get_product_name(self, response):
        return response.css('h1.product_title::text').get()
    
    def get_product_category(self, response):
        return response.css('nav.sp-breadcrumb a::text').getall()[1]
    
    def get_product_sku(self, response):
        return response.css('span#pr_sku_ppr::text').get()
    
    def get_product_price(self, response):
        return response.css('span.money::text').get()
    
    def get_product_availability(self, response):
        return response.css('span.js_in_stock::text').get()
    
    def get_product_available_sizes(self, response):
        return response.css('ul.swatches-select li::attr(data-value)').getall()
    
    def get_product_details(self, response):
        return response.css('section#content1 p::text').getall()
    
    def get_product_size_chart(self, response):
        return response.css('section#content2 ::text').getall()
    
    def get_shipping_return_policy(self, response):
        return response.css('section#content4 ::text').getall()
    
    def get_next_page_url(self, response):
        if response.css("link[rel='next']::attr(href)").get():
            return self.start_urls[0] + response.css("link[rel='next']::attr(href)").get()
        return False
    