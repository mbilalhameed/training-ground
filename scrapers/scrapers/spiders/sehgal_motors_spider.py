import re
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor

class SehgalMotorSpider(CrawlSpider):
    
    name = 'sehgalmotors'
    start_urls = ['https://www.sehgalmotors.pk/', ]
    allowed_domain = 'sehgalmotors.pk'
    
    rules = (
        Rule(LinkExtractor(restrict_css="div.section_area"), callback="parse_product", follow=True),
        Rule(LinkExtractor(restrict_css="ul.dropdown-menu"), follow=True)
    )
    
    regex = re.compile(r'[\n\r\t ]+')

    def parse_product(self, response):
        yield self.scrap_product(response)
        
    def scrap_product(self, response):
        product = self.get_products(response)
        try:
            product_sku = self.get_product_sku(product)
        except IndexError:
            return {}
        
        product_name = self.get_product_name(product)
        product_category = self.get_product_category(product)
        product_info = self.get_product_info(product)
        product_price = self.get_product_price(product)
        product_images = self.get_product_images(product)
        product_bread_crumbs = self.get_product_breadcrumbs(product)
        
        return {
            'product_sku': product_sku,
            'product_category': product_category,
            'product_name': product_name,
            'product_price': product_price,
            'product_images': product_images,
            'product_bread_crumbs': product_bread_crumbs,
            'product_info': product_info
        }

    def get_products(self, response):
        return response.css('body')
    
    def get_product_category(self, product):
        return product.css('nav.header_area a::text').getall()
    
    def get_product_name(self, product):
        return product.css('div.slider_bottomside b::text').get()
    
    def get_product_price(self, product):
        return product.css('div.p-price::attr(productprice)').get()
    
    def get_product_images(self, product):
        return product.css('div.carousel-inner img::attr(src)').getall()
    
    def get_product_sku(self, product):
        return product.css('div.slider_bottomside b::text').getall()[1]
    
    def get_product_breadcrumbs(self, product):
        return product.css('nav.header_area a::text').getall()
    
    def get_products_description(self, description_selector):
        return ' '.join(description_selector.css('::text').getall())
    
    def get_products_features(self, features_selector):
        return ' '.join(features_selector.css('::text').getall())
    
    def get_products_care_info(self, care_info_selector):
        return ' '.join(care_info_selector.css('::text').getall())
    
    def get_products_installation(self, installation_selector):
        return ' '.join(installation_selector.css('::text').getall())
    
    def get_product_info(self, product):
        product_info_selectors = product.css('.resp-tabs-container .resp_tab')
        product_description = self.get_products_description(product_info_selectors[0])
        product_features = self.get_products_description(product_info_selectors[1])
        product_care_info = self.get_products_description(product_info_selectors[2])
        product_installation = self.get_products_description(product_info_selectors[3])
        
        return {
            'product_description': self.regex.sub(" ", product_description),
            'product_features': self.regex.sub(" ", product_features),
            'product_care_info': self.regex.sub(" ", product_care_info),
            'product_installation': self.regex.sub(" ", product_installation)
        }
