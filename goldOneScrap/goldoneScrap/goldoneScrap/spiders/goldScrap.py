import scrapy

class GoldscrapSpider(scrapy.Spider):
    name = "goldScrap"
    allowed_domains = ["www.goldonecomputer.com"]
    start_urls = ["https://www.goldonecomputer.com/"]  

    def parse(self, response):
        category = response.xpath("//ul[@class='dropmenu']/li")
        for cat in category:
            name = cat.xpath("./a/text()").get()
            url = cat.xpath("./a/@href").get()
            yield (response.follow(url,callback=self.products,meta={'category-name':name}))

    def products(self,response):
        category_name = response.meta['category-name']
        product = response.xpath("//div[@class='row']//div[@class='product-block-inner']/div[@class = 'image']//a/@href")
        for pro in product:
            yield (response.follow(pro.get(),callback=self.products_details,meta = {'category-name':category_name}))
        
        next_page = response.xpath("//ul[@class='pagination']/li[@class='active']/following-sibling::li/a/@href").get()
        if next_page is not None:
            next_page_url = next_page
            yield response.follow(next_page_url,callback = self.products,meta = {'category-name':category_name})
    
    def products_details(self,response):
        category_name = response.meta['category-name']
        product_name = response.xpath("//div[contains(@class,'product-right')]/h3/text()").get()
        product_price = response.xpath("//ul[contains(@class,'price')]/li")
        final_price = ""
        for price in product_price:
            old_price = price.xpath(".//span//text()").get()
            if(old_price is None or old_price==""):
                old_price = price.xpath(".//h3/text()").get()
            print(old_price)
            special_price = price.xpath(".//h3[@class='special-price']//text()").get()
            if special_price is None :
                final_price = old_price
            else:
                final_price = special_price

        brand = response.xpath("//div[@class='col-sm-6 product-right']//ul[@class='list-unstyled']/li/a/text()").get()
        product_code = response.xpath("//div[@class='col-sm-6 product-right']//ul[@class='list-unstyled']/li/text()").get().strip()
        image = response.xpath("//div[@class='image']//img[@id='tmzoom']/@src").get()
        review_count = response.xpath("//a[@class='review-count']/text()").get().split(" ")[0]
        product_details = {
            'Product Name': product_name,
            'Final Price': final_price,
            'Brand': brand,
            'Product Code': product_code,
            'Image': image,
            'Review Count': review_count
        }

        yield {
            'Category Name': category_name,
            'Product Details': product_details
        }




