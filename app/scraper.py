from parsel import Selector
import asyncio
import httpx
from config import DEFAULT_HEADERS
from mongo_db.mongo_database import Mongo_DB
from db.models import RezkaSeriesModel
from db.database import Database
from async_redis.redis_db import Redis_DB


class RezkaSeriesScraper:
    MAIN_URL = "https://rezka.ag/series/thriller/page/{}/"
    SERIAL_URL = '//div[@class="b-content__inline_item-cover"]/a/@href'
    SERIAL_DETAIL_URL = '//div[@class="b-post"]/meta/@content'
    TITLE = '//div[@class="b-post__title"]/h1[@itemprop="name"]/text()'
    RELEASE_YEAR = '//div[@class="b-post__infotable_right_inner"]//td/a/text()'
    COUNTRY = '//table[@class="b-post__info"]/tbody/tr[2]/td[2]/a/text()'  # none
    GENRE = '//td/a/span[@itemprop="genre"]/text()'
    AGE_GROUP = '//tbody//tr[6]//td[2]/span[@class="bold"]/text()'  # none
    DURATION = '//td[@itemprop="duration"]/text()'
    IMAGE = '//img[@itemprop="image"]/@src'

    def __init__(self):
        self.all_pages = []
        self.all_urls = []
        self.redis_data = []
        self.redis_database = Redis_DB()
        self.mongo_database = Mongo_DB()
        self.database = Database()

    async def get_all_pages(self):
        for i in range(1, 2):
            self.all_pages.append(self.MAIN_URL.format(i))
        for one_page in self.all_pages:
            content = httpx.get(one_page, headers=DEFAULT_HEADERS).text
            page_selector = Selector(text=content)
            self.all_urls.extend(page_selector.xpath(self.SERIAL_URL).extract())

    async def get_url(self, client, url):
        response = await client.get(url)
        await self.save_data(response.text)
        return response

    async def parse_data(self):
        async with httpx.AsyncClient(headers=DEFAULT_HEADERS) as client:
            tasks = []
            for url in self.all_urls:
                tasks.append(asyncio.create_task(self.get_url(client, url)))
            serial_gather = await asyncio.gather(*tasks)
            await client.aclose()

    async def save_data(self, content):
        tree = Selector(text=content)
        url = tree.xpath(self.SERIAL_DETAIL_URL).extract_first()
        title = tree.xpath(self.TITLE).extract_first()
        release_year = tree.xpath(self.RELEASE_YEAR).extract_first()
        country = tree.xpath(self.COUNTRY).extract_first()
        genre = tree.xpath(self.GENRE).extract_first()
        age_group = tree.xpath(self.AGE_GROUP).extract_first()
        duration = tree.xpath(self.DURATION).extract_first()
        image = tree.xpath(self.IMAGE).extract_first()

        mongo_data = Mongo_DB.log_collection = {
            "current url": url,
            "date": Mongo_DB.log_collection.get("date"),
        }
        # print(mongo_data)
        # await self.mongo_database.add_to_log_collection(log_objects=mongo_data)

        postgresql_data = RezkaSeriesModel(
            current_url=url,
            title=title,
            release_year=release_year,
            country=country,
            genre=genre,
            age_group=age_group,
            duration=duration,
            image=image,
        )
        self.database.add_series(objects=postgresql_data)

        redis_data = Redis_DB.redis_url_data = {
            "url": url,
            "date": Redis_DB.redis_url_data.get("date"),
        }
        print(redis_data)
        await self.redis_database.add_to_redis_db(redis_objects=redis_data)

    async def main(self):
        await self.get_all_pages()
        await self.parse_data()


if __name__ == "__main__":
    scraper = RezkaSeriesScraper()
    asyncio.run(scraper.main())
