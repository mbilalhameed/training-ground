import re
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor

class ComputerZone(CrawlSpider):
    
    name = 'czone'
    start_urls = ['https://www.czone.com.pk/', ]
    allowed_domain = 'czone.com.pk'
    
    regex = re.compile(r'[\n\r\t ]+')
    
    rules = (
        Rule(LinkExtractor(restrict_css="div.product"), callback="parse_product", follow=True),
        Rule(LinkExtractor(restrict_css="ul.pagination a.PageNumber"), follow=True),
        Rule(LinkExtractor(restrict_css=".megamenu-content li.child"), follow=True)
    )

    def parse_product(self, response):
        yield self.scrap_product(response)
    
    def scrap_product(self, response):
        
        product_url = self.get_product_url(response)
        product_category = self.get_product_category(response)
        product_type = self.get_product_type(response)
        product_brand = self.get_product_brand(response)
        product_name = self.get_product_name(response)
        product_code = self.get_product_code(response)
        product_price = self.get_product_price(response)
        product_images = self.get_product_images(response)
        product_description = self.get_product_description(response)
        product_highlights = self.get_product_highlights(response)
        product_overview = self.get_product_overview(response)
        
        
        return {
            'product_url': product_url,
            'product_category': product_category,
            'product_type': product_type,
            'product_brand': product_brand,
            'product_name': product_name,
            'product_code': product_code,
            'product_price': product_price,
            'product_images': product_images,
            'product_description': self.regex.sub(" ", product_description),
            'product_highlights': self.regex.sub(" ", product_highlights),
            'product_overview': self.regex.sub(" ", product_overview),
        }
    
    def get_product_category(self, product):
        return product.css('span#spnParentProductType::text').get()
    
    def get_product_type(self, product):
        return product.css('span#spnProductType::text').get()
    
    def get_product_name(self, product):
        return product.css('h1.product-title::text').get()
    
    def get_product_price(self, product):
        return product.css('span#spnCurrentPrice::text').get()
    
    def get_product_images(self, product):
        return product.css('div.zoomThumbs a::attr(href)').getall()
    
    def get_product_code(self, product):
        return product.css('span#spnProductCode::text').get()
    
    def get_product_breadcrumbs(self, product):
        return product.css('ul.breadcrumb ::text').getall()
    
    def get_product_brand(self, product):
        return product.css('span#spnBrand::text').get()
    
    def get_product_description(self, product):
        return ' '.join(product.css('div.details-description ::text').getall())
    
    def get_product_highlights(self, product):
        return ' '.join(product.css('div#divProductHighlights ::text').getall())
    
    def get_product_overview(self, product):
        return ' '.join(product.css('div.product-overview ::text').getall())
    
    def get_product_url(self, product):
        return product.url
