import scrapy


class KijijiscraperSpider(scrapy.Spider):
    name = 'kijijiScraper'
    handle_httpstatus_all = True
    user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
    
    def start_requests(self):
        url = 'https://www.kijiji.ca/b-room-rental-roommate/city-of-toronto/page-1/c36l1700273?radius=14.0&price=460__600&address=Toronto%2C+ON&ll=43.653226,-79.383184'
        url = url.replace('/page-2/','/page-{}/')
        for i in range(1, 15):
            yield scrapy.Request(url=url.format(i), callback=self.after_fetch)


    def after_fetch(self, response):
        posting_links = response.css('a.title::attr(href)').extract()
        for link in posting_links:
            yield response.follow(url=link, callback=self.parse)
    
    
    def parse(self, response):
        title = " ".join(response.css('h1 ::text').extract())
        if title is None:
            title = '0'
        else:
            title = title.strip().lower()
        if response.css('h1 ::text') is None:
            return None
        
        yield {'title': title,
               'price': response.css('[class^="priceContainer"]').css('span::text').get(),
               'url': response.request.url,
               'description': " ".join(response.css('p ::text').getall()).strip().lower().replace('\n',' '),
               'address': response.css('[itemprop="address"]').css('span::text').get(),          
        }
        