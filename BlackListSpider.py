

# Imports
import scrapy
from scrapy.crawler import CrawlerProcess
import logging
logging.getLogger('scrapy').propagate = False
import pandas as pd


class BlackListSpider(scrapy.Spider):
    # Name of the spider
    name = 'Black_List_IP_Spider'

    # urls to crawl
    start_urls = [
        'https://www.sslproxies.org/'
    ]

    def parse(self, response):
        try:
            print('==========================================================================')
            print('\t\t### - Black List Ip Spider - ###')
            print('==========================================================================')
            # check if response status is ok(200)
            if response.status == 200:
                print("(Black list Ip) Status Code : {}".format(response.status))

                some_data = response.css('td:nth-child(1)::text').extract()
                ip_list = []
                for ip in some_data:
                    ip_list.append(ip)

                ip_dict = dict()
                ip_dict['IP'] = ip_list
                df = pd.DataFrame(data=ip_dict)
                df.to_csv('Black_List_IPS.csv', index=False)
                print("** BlackList Saved **")
            else:
                print('(Black list Ip) Response Code is : {}'.format(response.status))
        except Exception as e:
            print("(Black list Ip) " + str(e))


# Run Spider
process = CrawlerProcess()
process.crawl(BlackListSpider)
process.start()
