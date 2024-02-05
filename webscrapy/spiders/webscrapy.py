import json
import scrapy

from ..items import Link1Data, Link2Data, Link3Data
class webscrapy(scrapy.Spider):
    name = 'webscrapy'
    allowed_domains = ['www.scrapethissite.com']
    start_urls = ['https://www.scrapethissite.com/pages/']

    def parse(self, response):
        all_urls = response.xpath("//a/@href").extract()
        for url in all_urls:
            processed_url = response.urljoin(url)
            match url:
                case "/pages/simple/":
                    yield scrapy.Request(processed_url, callback=self.parse_link1)
                case "/pages/forms/":
                    yield scrapy.Request(processed_url, callback=self.parse_link2)
                case "/pages/ajax-javascript/":
                    yield scrapy.Request(processed_url, callback=self.parse_link3)

    def parse_link1(self,response): 
        item = Link1Data()
        for country in response.xpath('//div[@class="col-md-4 country"]'):
            item['country_name'] = country.xpath('.//h3[@class="country-name"]/text()').extract()[1].strip()
            item['country_capital'] = country.xpath('.//span[@class="country-capital"]/text()').extract()
            item['country_population'] = country.xpath('.//span[@class="country-population"]/text()').extract()
            item['country_area'] = country.xpath('.//span[@class="country-area"]/text()').extract()
            yield item

    def parse_link2(self,response): 
        item = Link2Data()
        for team_row in response.xpath('//tr[@class="team"]'):
            item['team_name'] = team_row.xpath('.//td[@class="name"]/text()').get(default='').strip()
            item['year'] = team_row.xpath('.//td[@class="year"]/text()').get(default='').strip()
            item['wins'] = team_row.xpath('.//td[@class="wins"]/text()').get(default='').strip()
            item['losses'] = team_row.xpath('.//td[@class="losses"]/text()').get(default='').strip()
            item['ot_losses'] = team_row.xpath('.//td[@class="ot-losses"]/text()').get(default='').strip()
            item['gf'] = team_row.xpath('.//td[@class="gf"]/text()').get(default='').strip()
            item['ga'] = team_row.xpath('.//td[@class="ga"]/text()').get(default='').strip()
            item['total'] = team_row.xpath('.//td[@class="diff text-success"]/text()').get(default='').strip()
            yield item
        #pagination_links = response.xpath('//ul[@class="pagination"]/li/a/@href').getall()
        for link in response.xpath('//ul[@class="pagination"]/li/a/@href').getall():
            page_num = link.split('=')[-1]
            next_page_url = f'https://www.scrapethissite.com/pages/forms/?page_num={page_num}'
            yield scrapy.Request(url=next_page_url, callback=self.parse_link2)

    def parse_link3(self, response):
        ajax_years = ['2015', '2014', '2013', '2012', '2011', '2010']
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }
        for year in ajax_years:
            ajax_url = f'https://www.scrapethissite.com/pages/ajax-javascript/?ajax=true&year={year}'
            yield scrapy.Request(url=ajax_url,method='GET',headers=headers, callback=self.parse_link3)

        try:
            data = json.loads(response.body)
            self.logger.info(f'JSON Data: {data}')
            for film in data:
                item = Link3Data()
                item['filmyear'] = film.xpath('.//a[@class="year-link"]/text()').get(default='').strip()
                item['filmtitle'] = film.xpath('.//div[@class="film-title"]/text()').get(default='')
                item['filmnom'] = film.xpath('.//div[@class="film-nominations"]/text()').get(default='').strip()
                item['filmawards'] = film.xpath('.//div[@class="film-awards"]/text()').get(default='').strip()
                item['filmbest'] = film.xpath('.//div[@class="film-best-picture"]/text()').get(default='').strip()
                yield item

            next_page = data.get('next_page')
            if next_page:
                yield scrapy.Request(next_page, callback=self.parse_ajaxjavascript)

        except json.JSONDecodeError as e:
            self.logger.error(f'Error decoding JSON: {e}')
