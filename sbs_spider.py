import scrapy
from sbs.spiders.items import SbsOverview
from scrapy.loader import ItemLoader


class SbsSpider(scrapy.Spider):
    name = 'sbs_spider'
    allowed_domains = ['sbs.nhs.uk']
    start_urls = ['https://sbs.nhs.uk/proc-framework-agreements-support']

    def parse(self, response):
        urls = response.css('h3>a::attr(href)')[0:4].extract()
        for url in urls:
            url = response.urljoin(url)
            yield scrapy.Request(url=url, callback=self.parse_services)

    def parse_services(self, response):
        urls = response.css('p>a.a_body__link::attr(href)').extract()
        for url in urls:
            if '/fas' in url:
                url = response.urljoin(url)
                yield scrapy.Request(url=url, callback=self.parse_items)
            elif '/ica' in url:
                url = response.urljoin(url)
                yield scrapy.Request(url=url, callback=self.parse_items)
            else:
                pass

    def parse_items(self, response):
        l = ItemLoader(item=SbsOverview(), selector=response)
        l.add_css('code', 'p>span::text')
        l.add_value('organisation', 'sbs')
        l.add_value('url', response.url)
        l.add_xpath('category', '/html/body/header/div[3]/div/ol/li[5]/a//text()')
        l.add_xpath('description', '/html/body/main/div/div[3]/div/p[2]//text()')
        l.add_css('framework_title', 'h1.a-heading__title::text')
        l.add_css('start_date', 'p:nth-child(6)::text')
        l.add_css('start_date', 'p:nth-child(7)::text')
        l.add_css('start_date', 'p:nth-child(8)::text')
        l.add_css('start_date', 'p:nth-child(9)::text')
        l.add_css('start_date', 'p:nth-child(11)::text')
        l.add_css('start_date', 'p:nth-child(14)::text')
        l.add_css('start_date', 'tr>td>p:nth-child(2)::text')
        l.add_css('end_date', 'p:nth-child(6)::text')
        l.add_css('end_date', 'p:nth-child(7)::text')
        l.add_css('end_date', 'p:nth-child(8)::text')
        l.add_css('end_date', 'p:nth-child(9)::text')
        l.add_css('end_date', 'p:nth-child(11)::text')
        l.add_css('end_date', 'p:nth-child(14)::text')
        l.add_css('end_date', 'tr>td>p:nth-child(2)::text')
        l.add_css('extension_options', 'p:nth-child(7)::text')
        l.add_css('extension_options', 'p:nth-child(8)::text')
        l.add_css('extension_options', 'p:nth-child(9)::text')
        l.add_css('lot_number', 'span.procgreentext::text')
        l.add_css('lot_description', 'span.procgreentext::text')
        l.add_css('lot_number', '.p:nth-child(12)::text')
        l.add_css('lot_description', 'p:nth-child(12)::text')
        l.add_css('lot_number', 'p:nth-child(10)>a::text')
        l.add_css('lot_description', 'p:nth-child(10)>a::text')
        l.add_xpath('supplier_name', '//td/p/a//text()')
        yield l.load_item()
