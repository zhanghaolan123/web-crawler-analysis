import scrapy
from scrapy.crawler import CrawlerProcess

class ZhaopinSpider(scrapy.Spider):
    name = 'zhaopin'
    start_urls = ['https://www.zhaopin.com/python爬虫工程师/']

    def parse(self, response):
        for job in response.css('div.job-item'):
            yield {
                'title': job.css('h3::text').get().strip(),
                'salary': job.css('span.salary::text').get(),
                'skills': job.css('div.skill-tag::text').getall(),
                'company': job.css('a.company-name::text').get()
            }
        next_page = response.css('a.next-page::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)

# 运行爬虫并保存数据到data目录
process = CrawlerProcess(settings={
    'FEED_FORMAT': 'json',
    'FEED_URI': '../data/jobs.json',
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'DOWNLOAD_DELAY': 2  # 遵守反爬规则
})
process.crawl(ZhaopinSpider)
process.start()
