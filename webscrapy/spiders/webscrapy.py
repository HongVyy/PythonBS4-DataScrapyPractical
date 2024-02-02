import scrapy
from ..items import WebscrapyItem
from scrapy_splash import SplashRequest

class webscrapy(scrapy.Spider):
    name = 'webscrapy'
    allowed_domains = ['www.scrapethissite.com']
    start_urls = ['https://www.scrapethissite.com/pages/']

    def parse(self, response):
        urls = response.css("a::attr(href)").extract()
        for url in urls:
            processed_url = response.urljoin(url)
            match url:
                case "/pages/simple/":
                    yield response.follow(processed_url, callback=self.parse_link1)
                case "/pages/forms/":
                    yield response.follow(processed_url, callback=self.parse_link2)
                case "/pages/ajax-javascript/":
                    yield response.follow(processed_url, callback=self.parse_link3)
                case "/pages/frames/":
                    yield response.follow(processed_url, callback=self.parse_link4)
                case "/pages/advanced/":
                    yield response.follow(processed_url, callback=self.parse_link5)

    def parse_link1(self, response): 
        for country in response.css('div.col-md-4.country'):
            yield {
                'Country Name': country.css('h3.country-name::text').get(default='').strip(),
                'Country Capital': country.css('span.country-capital::text').get(default='').strip(),
                'Country Population': country.css('span.country-population::text').get(default='').strip(),
                'Country Area': country.css('span.country-area::text').get(default='').strip(),
            }

    def parse_link2(self, response): 
        for team in response.css('tr.team'):
            yield {
                "Team Name": team.css('td.name::text').get(default='').strip(),
                "Year": team.css('td.year::text').get(default='').strip(),
                "Wins": team.css('td.wins::text').get(default='').strip(),
                "Losses": team.css('td.losses::text').get(default='').strip(),
                "OT Losses": team.css('td.ot-losses::text').get(default='').strip(),
                "Win %": team.css('td.pct.text-success::text').get(default='').strip(),
                "GF": team.css('td.gf::text').get(default='').strip(),
                "GA": team.css('td.ga::text').get(default='').strip(),
            }

    def parse_link3(self, response):
        film_year = response.css("a.year-link::text").get(default='').strip()
        for film in response.css('div.col-md-12'):
            yield {
                "Film Year": film_year,
                'Film Title': film.css('td.film-title::text').get(default='').strip(),
                'Film Nominations': film.css('td.film-nominations::text').get(default='').strip(),
                'Film Awards': film.css('td.film-awards::text').get(default='').strip(),
                'Film Best Picture': film.css('td.film-best-picture::text').get(default='').strip(),
            }

    def parse_link4(self, response):
        for turtle in response.css('div.col-md-4.turtle-family-card'):
            item = WebscrapyItem()
            item['image_url'] = turtle.css('img.turtle-image::attr(src)').get(default='')
            item['turtle_family_name'] = turtle.css('h3.family-name::text').get(default='').strip()
            item['learnmore_url'] = response.css('a.btn.btn-default.btn-xs::attr(href)').get(default='')
            yield item

    def parse_link5(self, response):
        yield {
            'link_text': response.css('a[target="_blank"]::text()').get(default='').strip(),
        }
