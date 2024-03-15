import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class ThanhnienSpider(CrawlSpider):
    name = 'thanhnien'
    allowed_domains = ['thanhnien.vn']
    start_urls = [
        'https://thanhnien.vn/thoi-su.htm',
        'https://thanhnien.vn/the-gioi.htm',
    ]
    rules = (
        Rule(LinkExtractor(allow=r'.*\.htm$'), callback='parse_article', follow=True),
    )
    def parse_article(self, response):
        item = {
            'url': response.url,
            'title': response.xpath('//h1[@class="details__headline"]/text()').get(),
            'description': response.xpath('//meta[@property="og:description"]/@content').get(),
            'category': response.xpath('//meta[@property="article:section"]/@content').get(),
            'published_date': response.xpath('//div[@class="details__meta"]/span[@class="meta time"]/text()').get(),
            'author': response.xpath('//div[@class="details__meta"]/span[@class="meta author"]/a/text()').get(),
            'content': '\n'.join(response.css('div[class^="details__body"] p::text').getall()),
        }
        yield item

    def parse_start_url(self, response):
        category_urls = response.xpath('//ul[@class="menu-nav"]/li/a/@href').getall()
        for url in category_urls:
            if url == "/":
                continue
            processed_url = response.urljoin(url)
            yield scrapy.Request(processed_url, callback=self.parse_category, meta={'current_page': 1})

    def parse_category(self, response):
        current_page = response.meta['current_page']
        if current_page > 100:
            return
        article_urls = response.xpath('//h2[@class="story__heading"]/a/@href').getall()
        for url in article_urls:
            processed_url = response.urljoin(url)
            yield scrapy.Request(processed_url, callback=self.parse_article)
        
        next_page = response.css('a.next-page::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse_category, meta={'current_page': current_page + 1})

