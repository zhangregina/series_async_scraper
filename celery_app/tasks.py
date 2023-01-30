from django.views.decorators.csrf import csrf_exempt

from main.celery import app


@app.task
@csrf_exempt
def start_scraping():
    print("hello from celery")
