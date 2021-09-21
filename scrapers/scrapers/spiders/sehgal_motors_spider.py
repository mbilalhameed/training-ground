import re
import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor


class SehgalMotorSpider(scrapy.Spider):
    
    name = 'sehgalmotors'
    start_urls = ['https://www.sehgalmotors.pk/', ]
    allowed_domain = 'sehgalmotors.pk'
    link_extractor = LinkExtractor(allow='product/', allow_domains= allowed_domain)
    rules = [Rule(link_extractor=link_extractor, callback='parse', follow=True)]
    regex = re.compile(r'[\n\r\t ]+')

    def parse(self, response):
        try:
            product = self.get_products(response)
            product_sku = self.get_product_sku(product)
            product_category = self.get_product_category(product)
            product_name = self.get_product_name(product)
            product_price = self.get_product_price(product)
            product_images = self.get_product_images(product)
            product_bread_crumbs = self.get_product_breadcrumbs(product)
            product_info = self.get_product_info(product)
            
            yield{
                'Product SKU': product_sku,
                'Product Category': product_category,
                'Product Name': product_name,
                'Product Price': product_price,
                'Product Images': product_images,
                'Product Bread Crumbs': product_bread_crumbs,
                'Product Usage Info': product_info
            }
            
        except IndexError:
            pass
        
        for link in self.link_extractor.extract_links(response):
            yield scrapy.Request(link.url, callback=self.parse)


    def get_products(self, response):
        return response.css('body')
    
    
    def get_product_category(self, product):
        return product.css('nav.header_area a::text').getall()[1]
    
    
    def get_product_sub_category(self, product):
        return product.css('h1::attr(producttitle)').get()
    
    
    def get_product_name(self, product):
        return product.css('div.slider_bottomside b::text').getall()[0]
    
    
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
            'Description': self.regex.sub(" ", product_description),
            'Features': self.regex.sub(" ", product_features),
            'Care Info': self.regex.sub(" ", product_care_info),
            'Installation': self.regex.sub(" ", product_installation)
        }
