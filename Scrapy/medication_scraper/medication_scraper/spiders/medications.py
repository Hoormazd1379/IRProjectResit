import scrapy
from medication_scraper.items import MedicationItem

class MedicationsSpider(scrapy.Spider):
    name = "medications"
    allowed_domains = ["www.drugs.com"]
    start_urls = [
        "https://www.drugs.com/alpha/a.html",
        "https://www.drugs.com/alpha/b.html",
        # Add more URLs for other letters if needed
    ]

    def parse(self, response):
        # Extract the URLs of medication pages from the current page
        medication_urls = response.xpath('.ddc-mgb-2 ul a::attr(href)').extract()
        
        for url in medication_urls:
            yield response.follow(url, callback=self.parse_page)
    
    def parse_medication(self, response):
        medication_urls = response.xpath('#content .ddc-list-unstyled a::attr(href)').extract()
        
        for url in medication_urls:
            yield response.follow(url, callback=self.parse_medication)

    def parse_medication(self, response):
        item = MedicationItem()
        
        # Populate item fields
        item['source'] = "drugs.com"
        item['source_url'] = response.url
        item['name'] = response.xpath('//h1/text()').get()
        item['generic_name'] = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "drug-subtitle", " " ))]/text()').get()
        item['description'] = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "drug-subtitle", " " ))]/text()').get()
        item['warnings'] = response.xpath('//*[@id="s-34071-1"]//*[contains(concat( " ", @class, " " ), concat( " ", "First", " " ))]/text()').get()
        item['side_effects'] = response.xpath('//*[@id="s-34084-4"]//*[contains(concat( " ", @class, " " ), concat( " ", "First", " " ))]/text()').get()
        item['how_to_take'] = response.xpath('//*[@id="s-34068-7"]//p/text()').getall()

        yield item
