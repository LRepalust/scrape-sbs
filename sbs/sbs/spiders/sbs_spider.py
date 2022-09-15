import re
import scrapy
from sbs.items import SbsItems, SbsItemLoader



class SbsSpider(scrapy.Spider):
    name = 'sbs_spider'
    allowed_domains = ['sbs.nhs.uk']
    start_urls = ['https://sbs.nhs.uk/proc-framework-agreements-support']

    def parse(self, response):
        category_urls = response.css('#maincontent .container + .a-panel.a-panel--list a.item__link::attr(href)').getall()
        for category_url in category_urls:
            category_url = response.urljoin(category_url)
            yield scrapy.Request(url=category_url, callback=self.parse_services)

    def parse_services(self, response):
        framework_urls = response.css(
            'a.a_body__link::attr(href)').getall()
        for framework_url in framework_urls:
            if '/fas' in framework_url:
                framework_url = response.urljoin(framework_url)
                yield scrapy.Request(url=framework_url, callback=self.parse_items)
            elif '/ica' in framework_url:
                framework_url = response.urljoin(framework_url)
                yield scrapy.Request(url=framework_url, callback=self.parse_items)
            else:
                pass

    def parse_items(self, response):
        loader = SbsItemLoader(item=SbsItems(), selector=response)
        loader.add_css('code', 'p>span::text')
        loader.add_value('organisation', 'sbs')
        loader.add_value('url', response.url)
        loader.add_xpath('category', '/html/body/header/div[3]/div/ol/li[5]/a//text()')
        loader.add_xpath('description', '/html/body/main/div/div[3]/div/p[2]//text()')
        loader.add_css('framework_title', 'h1.a-heading__title::text')
        loader.add_css('start_date', 'p:nth-child(6)')
        loader.add_css('start_date', 'p:nth-child(7)::text')
        loader.add_css('start_date', 'p:nth-child(8)::text')
        loader.add_css('start_date', 'p:nth-child(9)::text')
        loader.add_css('start_date', 'p:nth-child(11)::text')
        loader.add_css('start_date', 'p:nth-child(14)::text')
        loader.add_css('start_date', 'tr>td>p:nth-child(2)::text')
        loader.add_css('end_date', 'p:nth-child(6)::text')
        loader.add_css('end_date', 'p:nth-child(7)::text')
        loader.add_css('end_date', 'p:nth-child(8)::text')
        loader.add_css('end_date', 'p:nth-child(9)::text')
        loader.add_css('end_date', 'p:nth-child(11)::text')
        loader.add_css('end_date', 'p:nth-child(14)::text')
        loader.add_css('end_date', 'tr>td>p:nth-child(2)::text')
        loader.add_css('extension_options', 'p:nth-child(7)::text')
        loader.add_css('extension_options', 'p:nth-child(8)::text')
        loader.add_css('extension_options', 'p:nth-child(9)::text')
        loader.add_css('lot_number', 'span.procgreentext::text')
        loader.add_css('lot_description', 'span.procgreentext::text')
        loader.add_css('lot_number', '.p:nth-child(12)::text')
        loader.add_css('lot_description', 'p:nth-child(12)::text')
        loader.add_css('lot_number', 'p:nth-child(10)>a::text')
        loader.add_css('lot_description', 'p:nth-child(10)>a::text')
        loader.add_xpath('supplier_name', '//td/p/a//text()')
        yield loader.load_item()
