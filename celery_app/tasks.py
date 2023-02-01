import asyncio
from django.views.decorators.csrf import csrf_exempt
from app.scraper import RezkaSeriesScraper
from main.celery import app


@app.task
@csrf_exempt
def start_scraping():
    scraper = RezkaSeriesScraper()
    asyncio.run(scraper.main())
