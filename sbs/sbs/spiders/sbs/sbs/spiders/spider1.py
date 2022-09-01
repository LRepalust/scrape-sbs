import scrapy
from items import SbsItem
from scrapy.loader import ItemLoader


class Spider1Spider(scrapy.Spider):
    name = 'spider1'
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
        l = ItemLoader(item=SbsItem(), selector=response)
        l.add_css('code', 'p>span::text')
        l.add_value('organisation', 'sbs')
        l.add_value('url', response.url)
        l.add_xpath('category', '/html/body/header/div[3]/div/ol/li[5]/a//text()')
        l.add_xpath('description', '/html/body/main/div/div[3]/div/p[2]//text()')
        l.add_css('framework_title', 'h1.a-heading__title::text')
        l.add_css('start_date', '.a-body__inner > p:nth-child(6)::text')
        l.add_css('start_date', '.a-body__inner > p:nth-child(7)::text')
        l.add_css('start_date', '.a-body__inner > p:nth-child(8)::text')
        l.add_css('start_date', '.a-body__inner > p:nth-child(9)::text')
        l.add_css('start_date', '.a-body__inner > p:nth-child(11)::text')
        l.add_css('start_date', '.a-body__inner > p:nth-child(14)::text')
        l.add_css('start_date', 'div.a-table:nth-child(9) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > p:nth-child(2)::text')
        l.add_css('end_date', '.a-body__inner > p:nth-child(6)::text')
        l.add_css('end_date', '.a-body__inner > p:nth-child(7)::text')
        l.add_css('end_date', '.a-body__inner > p:nth-child(8)::text')
        l.add_css('end_date', '.a-body__inner > p:nth-child(9)::text')
        l.add_css('end_date', '.a-body__inner > p:nth-child(11)::text')
        l.add_css('end_date', '.a-body__inner > p:nth-child(14)::text')
        l.add_css('end_date', 'div.a-table:nth-child(9) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > p:nth-child(2)::text')
        l.add_css('extension_options', '.a-body__inner > p:nth-child(7)::text')
        l.add_css('extension_options', '.a-body__inner > p:nth-child(8)::text')
        l.add_css('extension_options', '.a-body__inner > p:nth-child(9)::text')
        yield l.load_item()
