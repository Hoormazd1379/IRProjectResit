# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from medication_scraper.items import MedicationItem
import json
import csv

class MedicationScraperPipeline:
    def __init__(self):
        self.json_file = open('medications.json', 'w', encoding='utf-8')
        self.csv_file = open('medications.csv', 'w', encoding='utf-8', newline='')
        self.json_exporter = JsonExporter(self.json_file)
        self.csv_exporter = CsvExporter(self.csv_file)

    def process_item(self, item, spider):
        # Export the item to JSON file
        self.json_exporter.export_item(item)
        
        # Export the item to CSV file
        self.csv_exporter.export_item(item)
        
        return item

    def close_spider(self, spider):
        # Close the JSON and CSV files
        self.json_file.close()
        self.csv_file.close()

class JsonExporter:
    def __init__(self, file):
        self.file = file

    def export_item(self, item):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

class CsvExporter:
    def __init__(self, file):
        self.file = file
        self.csv_writer = csv.DictWriter(file, fieldnames=MedicationItem.fields.keys())
        self.csv_writer.writeheader()

    def export_item(self, item):
        self.csv_writer.writerow(item)

