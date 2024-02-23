import scrapy
from scrapy.spiders import SitemapSpider
from ..items import ThanhniennewItem

class ThanhnienSpider(SitemapSpider):
    name = 'mynews'
    allowed_domains = ['thanhnien.vn']
    sitemap_urls = ['https://thanhnien.vn/sitemap.xml']
    sitemap_follow = ['/sitemaps/sitemaps-2024'] 

    handle_httpstatus_list = [404]
    def parse(self, response):
        if response.status == 404:
            self.logger.error("Sitemap not found: %s", response.url)
            return
        
        item = ThanhniennewItem()
        item['url'] = response.url
        item['description'] = response.xpath('//meta[@property="og:description"]/@content').get()
        item['category'] = response.xpath('//div[@class="detail-cate"]/a[@data-role="cate-name-parent"]/@title').get(default='') or response.xpath('//div[@class="detail-cate"]/a[@data-role="cate-name"]/@title').get(default='')
        item['title'] = response.xpath('//meta[@property="og:title"]/@content').get()
        item['published_date'] = response.xpath('//div[@class="detail-time"]/div[@data-role="publishdate"]/text()').get(default='').strip()
        item['author'] = response.xpath('//meta[@property="dable:author"]/@content').get()
        item['content'] = '\n'.join(response.xpath('//div[@class="detail-cmain"]//div[@data-role="content"]/p/text()').getall())        
        yield item
        
    def parse_sitemap(self, response, **kwargs):
        sitemap = super().parse_sitemap(response, **kwargs)
        for item in sitemap:
            if "2024" in item["loc"] and "sitemaps/sitemaps-2024" in item["loc"]:
                published_date = item.xpath("//published_date/text()").get()
                item['published_date'] = published_date
                yield item
