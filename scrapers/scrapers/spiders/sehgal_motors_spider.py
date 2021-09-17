import scrapy


class SehgalMotorSpider(scrapy.Spider):
    
    name = 'sehgalmotors'
    sehgal_motors_url = 'https://www.sehgalmotors.pk/'

    
    def start_requests(self):
        
        yield scrapy.Request(url=self.sehgal_motors_url, callback=self.parse)
        
        
    def get_products_info(self, response):
        return response.css('a.productLink')
    
    
    def get_product_category(self, response):
        return response.url.split('/')[-1]
    
    
    def get_product_sub_category(self, response):
        return response.url.split('/')[-2]
    
    
    def get_product_name(self, product):
        return product.css('p::attr(producttitle)').get()
    
    
    def get_product_price(self, product):
        return product.css('div::attr(productprice)').get()


    def parse(self, response):
        if not response.css('a.productLink'):
            pass
        
        products = self.get_products_info(response)
        
        for product in products:
            category = self.get_product_category(response)
            sub_category = self.get_product_sub_category(response)
            product_name = self.get_product_name(product)
            product_price = self.get_product_price(product)
            
            yield {
                'Category': category,
                'Sub-category': sub_category,
                'Product Name': product_name,
                'Product Price': product_price
            }
        
        for sub_category_link in response.css("ul.categoryList a::attr(href)").extract():
            sub_category_link = self.sehgal_motors_url+sub_category_link
            yield response.follow(sub_category_link, callback=self.parse)
