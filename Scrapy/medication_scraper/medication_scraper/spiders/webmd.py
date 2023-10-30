import scrapy
from medication_scraper.items import MedicationItem


class WebmdSpider(scrapy.Spider):
    name = "webmd"
    allowed_domains = ["www.webmd.com"]
    start_urls = []
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    for letter in alphabet:
        for l2 in alphabet:
            start_urls.append("https://www.webmd.com/drugs/2/alpha/"+letter+"/"+letter+l2)

    def parse(self, response):
        # Extract the URLs of medication pages from the current page
        medication_urls = response.css('.alpha-drug-name::attr(href)').extract()
        
        for url in medication_urls:
            yield response.follow(url, callback=self.parse_medication)

    def parse_medication(self, response):
        item = MedicationItem()
        
        # Populate item fields
        item['source'] = "webmd.com"
        item['source_url'] = response.url

        item['name'] = response.css('h1.drug-name::text').get().replace(" ", "")
        item['generic_name'] = response.css('.drug-generic-name').get()

        item['description'] = response.css('.monograph-content-see-more p').get()

        item['side_effects'] = response.css('.side-effects-container .monograph-content').get()

        item['warnings'] = response.css('.precautions-container .monograph-content').get()

        item['how_to_take'] = response.css('.lazy-load-see-more p').get()

        if (item['name'] != ''):
            item['id'] = item['name']+'_'+item['source']
            yield item