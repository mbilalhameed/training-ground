from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider

class ApolloSportsSpyder(CrawlSpider):
    
    name = 'apollosports'
    start_urls = ['https://www.apollosports.pk/', ]
    
    rules = (
        Rule(LinkExtractor(restrict_css="h2.woo-loop-product__title"), callback="parse_product", follow=True),
        Rule(LinkExtractor(restrict_css="div.mega-menu-content") ,follow=True),
    )
    
    def parse_product(self, response):
        yield self.get_product_info(response)
    
    def get_product_info(self, response):
        product_name = self.get_product_name(response)
        if not product_name:
            pass
        
        product_price = self.get_product_price(response)
        product_description = self.get_product_description(response)
        product_images = self.get_product_images(response)
        product_brand = self.get_product_brand(response)
        product_specification = self.get_product_specification(response)
        product_size_chart = self.get_product_size_chart(response)
        
        return {
            'product_name': product_name,
            'product_price': product_price,
            'product_description': product_description,
            'product_images': product_images,
            'product_brand': product_brand,
            'product_specification': product_specification,
            'product_size_chart': product_size_chart,
        }
        
    def get_product_name(self, response):
        return response.css('.entry-left h1.product_title::text').get()
    
    def get_product_price(self, response):
        return response.css('span.woocommerce-Price-amount bdi::text').get()
    
    def get_product_description(self, response):
        return response.css('div.woocommerce-product-details__short-description ::text').getall()
    
    def get_product_images(self, response):
        return response.css('div.woocommerce-product-gallery img::attr(src)').getall()
    
    def get_product_brand(self, response):
        return response.css('div.woocommerce-Tabs-panel h3::text').getall()
    
    def get_product_specification(self, response):
        return response.css('table.woocommerce-product-attributes ::text').getall()
    
    def get_product_size_chart(self, response):
        return response.css('div.yith-wcpsc-product-table-wrapper img::attr(src)').get()
