import scrapy


class QuotesSpider(scrapy.Spider):
    name = "imdb"
    start_urls = [
        'https://www.imdb.com/search/title/?release_date=2018-01-01,2018-12-31&sort=num_votes,desc&start=1000&ref_=adv_nxt',
    ]

    def parse(self, response):
        for data in response.css('.lister-item-content'):
            yield {
                'Serial Number': data.css('.lister-item-index::text').get(),
                'Movie': data.css('.lister-item-index+ a::text').get(),
                'Runtime': data.css('.runtime::text').get(),
            }

        next_page = response.css('.clear+ .desc .next-page::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
