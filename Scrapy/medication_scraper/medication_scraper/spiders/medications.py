import scrapy
from medication_scraper.items import MedicationItem

class MedicationsSpider(scrapy.Spider):
    name = "medications"
    allowed_domains = ["www.drugs.com"]
    start_urls = [
        "https://www.drugs.com/alpha/a.html",
        "https://www.drugs.com/alpha/b.html",
        "https://www.drugs.com/alpha/c.html",
        "https://www.drugs.com/alpha/d.html",
        "https://www.drugs.com/alpha/e.html",
        "https://www.drugs.com/alpha/f.html",
        "https://www.drugs.com/alpha/g.html",
        "https://www.drugs.com/alpha/h.html",
        "https://www.drugs.com/alpha/i.html",
        "https://www.drugs.com/alpha/j.html",
        "https://www.drugs.com/alpha/k.html",
        "https://www.drugs.com/alpha/l.html",
        "https://www.drugs.com/alpha/m.html",
        "https://www.drugs.com/alpha/n.html",
        "https://www.drugs.com/alpha/o.html",
        "https://www.drugs.com/alpha/p.html",
        "https://www.drugs.com/alpha/q.html",
        "https://www.drugs.com/alpha/r.html",
        "https://www.drugs.com/alpha/s.html",
        "https://www.drugs.com/alpha/t.html",
        "https://www.drugs.com/alpha/u.html",
        "https://www.drugs.com/alpha/v.html",
        "https://www.drugs.com/alpha/w.html",
        "https://www.drugs.com/alpha/x.html",
        "https://www.drugs.com/alpha/y.html",
        "https://www.drugs.com/alpha/z.html",
        "https://www.drugs.com/alpha/0-9.html",

        # Add more URLs for other letters if needed
    ]

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

        item['warnings'] = response.css('#warnings+ p').getall()
        if (item['warnings'] == ''):
            item['warnings'] = response.css('#s-34071-1 .First').getall()

        item['how_to_take'] = response.css('#dosage+ p').getall()
        if (item['how_to_take'] == ''):
            item['how_to_take'] = response.css('#s-34067-9 .First').getall()

        if (item['name'] != ''):
            yield item
