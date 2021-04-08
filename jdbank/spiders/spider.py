import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import JjdbankItem
from itemloaders.processors import TakeFirst

pattern = r'(\xa0)?'

class JjdbankSpider(scrapy.Spider):
	name = 'jdbank'
	start_urls = ['https://jdbank.com/press/']

	def parse(self, response):
		post_links = response.xpath('//div[@class="elementor-text-editor elementor-clearfix"]/ul/li/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		date = response.xpath('//time/@datetime').get().split('T')[0]
		title = response.xpath('//h1/text()').get()
		content = response.xpath('(//div[@class="elementor-text-editor elementor-clearfix"])[3]//text()[not (ancestor::a[contains(text(),"CLICK HERE")])]').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))

		item = ItemLoader(item=JjdbankItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()
