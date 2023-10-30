import scrapy
from medication_scraper.items import MedicationItem

class MedicationsSpider(scrapy.Spider):
    name = "medications"
    allowed_domains = ["www.drugs.com"]
    start_urls = []
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    for letter in alphabet:
        start_urls.append("https://www.drugs.com/alpha/"+letter+".html")
                          
    def parse(self, response):
        # Extract the URLs of medication pages from the current page
        medication_urls = response.css('.ddc-mgb-2 ul a::attr(href)').extract()
        
        for url in medication_urls:
            yield response.follow(url, callback=self.parse_page)
            yield response.follow(url, callback=self.parse_medication)
    
    def parse_page(self, response):
        medication_urls = response.css('#content .ddc-list-unstyled a::attr(href)').extract()
        
        for url in medication_urls:
            yield response.follow(url, callback=self.parse_medication)

    def parse_medication(self, response):
        item = MedicationItem()
        
        # Populate item fields
        item['source'] = "drugs.com"
        item['source_url'] = response.url
        item['name'] = response.css('h1::text').get()
        item['generic_name'] = response.css('.drug-subtitle').get()

        item['description'] = response.css('#uses + p').get()
        if (item['description'] == ''):
            item['description'] = response.css('#s-34089-3 .First').get()

        item['side_effects'] = response.css('#side-effects+ p').get()
        if (item['side_effects'] == ''):
            item['side_effects'] = response.css('#s-34084-4 .First').get()

        item['warnings'] = ""
        warnings = response.css('#warnings+ p').getall()
        if (len(warnings) == 0):
            warnings = response.css('#s-34071-1 .First').getall()
        for w in warnings:
            item['warnings'] += w

        item['how_to_take'] = ""
        how_to_take = response.css('#dosage+ p').getall()
        if (len(how_to_take) == 0):
            how_to_take = response.css('#s-34067-9 .First').getall()
        for htt in how_to_take:
            item['how_to_take'] += htt

        if (item['name'] != ''):
            item['id'] = item['name']+'_'+item['source']
            yield item
