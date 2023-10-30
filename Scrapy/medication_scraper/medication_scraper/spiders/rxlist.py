import scrapy
from medication_scraper.items import MedicationItem


class RxlistSpider(scrapy.Spider):
    name = "rxlist"
    allowed_domains = ["www.rxlist.com"]
    start_urls = []
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    for letter in alphabet:
        start_urls.append("https://www.rxlist.com/drugs/alpha_"+letter+".htm")

    def parse(self, response):
        # Extract the URLs of medication pages from the current page
        medication_urls = response.css('#AZ_container li a::attr(href)').extract()
        
        for url in medication_urls:
            yield response.follow(url, callback=self.parse_medication)

    def parse_medication(self, response):
        item = MedicationItem()
        
        # Populate item fields
        item['source'] = "rxlist.com"
        item['source_url'] = response.url

        item['name'] = response.css('h1::text').get().replace(" ", "").replace("\r", "").replace("\n", "")
        item['generic_name'] = ""
        generic_name = response.css('.hero li').getall()
        for gn in generic_name:
            item['generic_name'] += gn

        item['description'] = response.css('p:nth-child(2)').get()

        item['side_effects'] = ""
        side_effects = response.css('.monograph_cont li , .monograph_cont p:nth-child(4)').getall()
        for se in side_effects:
            item['side_effects'] += se

        item['warnings'] = response.css('.pageSection:nth-child(5) p').get()

        item['how_to_take'] = ""
        how_to_take = response.css('p:nth-child(7)').getall()
        for htt in how_to_take:
            item['how_to_take'] += htt

        if (item['name'] != ''):
            item['id'] = item['name']+'_'+item['source']
            yield item

